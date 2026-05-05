from django.db.models.aggregates import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from article_module.models import Article
from product_module.models import ProductBrand, Product
from utils.my_decorators import permission_checker_decorator_factory


# Create your views here.
@permission_checker_decorator_factory()
def dashboard(request):
    return render(request, 'admin_dashboard/dashboard_admin.html')


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class ArticleListView(ListView):
    model = Article
    template_name = 'admin_dashboard/article_list_admin.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset().prefetch_related('category')
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query

@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class ArticleEditView(UpdateView):
    model = Article
    template_name = 'admin_dashboard/article_edit_admin.html'
    fields = '__all__'
    success_url = reverse_lazy('article_list_admin')

@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'admin_dashboard/product_list_admin.html'
    context_object_name = 'products'
    paginate_by = 12
