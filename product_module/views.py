from types import SimpleNamespace

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from django.urls import reverse

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from site_module.models import Banner
from utils.conventors import group_list
from utils.http_service import get_client_ip
from .models import Product, ProductCategory, ProductBrand, ProductVisit


def _product_gallery_items(product: Product):
    rows = list(
        product.gallery_images.all().order_by('order', 'created_at')
    )
    if rows:
        return rows
    if product.image:
        return [
            SimpleNamespace(
                pk=0,
                image=product.image,
                image_alt=product.title,
                is_main=True,
            )
        ]
    return []


def _gallery_main_item(items):
    if not items:
        return None
    for row in items:
        if getattr(row, 'is_main', False):
            return row
    return items[0]


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'product_module/product_list.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = Banner.objects.filter(is_active=True, position__iexact=Banner.BannerPosition.product_list)

        selected_brands = self.request.GET.getlist('brands')
        context['selected_brands'] = selected_brands

        available_brands = ProductBrand.objects.filter(
            is_active=True,
            product_brands__isnull=False
        ).annotate(
            products_count=Count('product_brands')
        ).distinct()
        context['available_brands'] = available_brands

        return context

    def get_queryset(self, **kwargs):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        selected_brands = request.GET.getlist('brands')
        search_query = request.GET.get('q', '').strip()

        if start_price is not None and start_price != '':
            query = query.filter(price__gte=start_price)
        if end_price is not None and end_price != '':
            query = query.filter(price__lte=end_price)
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if selected_brands:
            query = query.filter(brand__url_title__in=selected_brands)
        if search_query:
            query = query.filter(title__icontains=search_query)
        return query

    # def get_queryset(self):
    #     base_query = super(ProductListView , self).get_queryset()
    #     data = base_query.filter(is_active=True)
    #     return data


# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all().order_by('-price')[:5]
#         return context

# def product_list(request):
#     products = Product.objects.all().order_by('-price')[:5]
#     context = {
#         'products': products,
#     }
#     return render(request, 'product_module/product_list.html', context)


# def product_detail(request, slug):
#     product = get_object_or_404(Product , slug=slug)
#     return render(request, 'product_module/product_detail.html', {'product': product})


# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = kwargs['slug']
#         context['product'] = get_object_or_404(Product , slug=slug)
#         return context

class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_queryset(self):
        return super().get_queryset().prefetch_related('gallery_images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        context['banners'] = Banner.objects.filter(is_active=True, position__iexact=Banner.BannerPosition.product_detail)
        
        gallery_items = _product_gallery_items(loaded_product)
        context['gallery_items'] = gallery_items
        context['gallery_main_item'] = _gallery_main_item(gallery_items)
        context['gallery_batches'] = group_list(gallery_items, 3)
        context['related_products'] = group_list(list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(id=loaded_product.id).order_by('-id')[:12]))
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, product_id=loaded_product.id, user_id=user_id)
            new_visit.save()
        return context

def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.prefetch_related('productcategory_set').filter(
        is_active=True, 
        is_delete=False, 
        category__isnull=True  # only get parent categories (no parent)
    )
    context = {'categories': product_categories}
    return render(request, 'product_module/components/product_categories_component.html', context)

def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product_brands')).filter(is_active=True)
    context = {'brands': product_brands}
    return render(request, 'product_module/components/product_brands_component.html', context)


def product_search_suggestions(request: HttpRequest):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        is_active=True,
        is_delete=False,
        title__icontains=query
    )[:6]

    results = [
        {
            'title': product.title,
            'url': product.get_absolute_url(),
            'price': product.price,
        }
        for product in products
    ]
    return JsonResponse({'results': results})
