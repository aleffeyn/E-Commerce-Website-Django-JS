from django.urls import path
from . import views

urlpatterns = [
    # path('' , views.product_list)
    # path('<slug:slug>' , views.product_detail , name='product_detail')

    path('', views.ProductListView.as_view() , name='product_list'),
    path('search/suggestions/', views.product_search_suggestions, name='product_search_suggestions'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_brands_list'),
    path('<slug:slug>' , views.ProductDetailView.as_view() , name='product_detail'),
]
