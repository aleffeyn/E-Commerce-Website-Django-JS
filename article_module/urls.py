from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view() , name='article_list'),
    path('cat/<str:category>', views.ArticleListView.as_view(), name='article_by_category_filter'),
    path('add-article-comment', views.add_article_comment, name='add_article_comment'),
    path('<pk>' , views.ArticleDetailView.as_view() , name='article_detail'),
]