from django.urls import path

from admin_dashboard import views

urlpatterns = [
    path('', views.dashboard , name='dashboard_admin'),
    path('articles/' , views.ArticleListView.as_view(), name='article_list_admin'),
    path('articles/<pk>' , views.ArticleEditView.as_view(), name='article_edit_admin'),
    path('products/' , views.ProductListView.as_view(), name='product_list_admin'),
]