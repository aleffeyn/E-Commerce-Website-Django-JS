from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from unicodedata import category

from article_module.models import Article, ArticleCategory, ArticleComment


# Create your views here.

class ArticleListView(ListView):
    model = Article
    article_list = Article.objects.filter(is_active=True)
    template_name = 'article_module/article_list_page.html'
    paginate_by = 3
    
    def get_context_data(self,*args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query

def article_filter_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,parent_id=None)
    context= {
        'article_main_categories': article_main_categories
    }
    return render(request, 'article_module/includes/article_filter_component.html', context)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_article = self.object

        context['previous_article'] = Article.objects.filter(
            is_active=True,
            id__lt=current_article.id
        ).order_by('-id').first()

        # Get the next article (newer)
        context['next_article'] = Article.objects.filter(
            is_active=True,
            id__gt=current_article.id
        ).order_by('id').first()

        context = super(ArticleDetailView, self).get_context_data()
        article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by('-created_at').prefetch_related('articlecomment_set')
        context['comment_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context


def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        
        if not article_comment or not article_comment.strip():
            return HttpResponse('نظر نمیتواند خالی باشد', status=400)
        
        print(article_id, article_comment, parent_id)
        new_comment = ArticleComment(article_id=article_id, comment=article_comment.strip(), user_id=request.user.id, parent_id=parent_id)
        new_comment.save()
        context={
            'comments' : ArticleComment.objects.filter(article_id=article_id, parent=None).order_by('-created_at').prefetch_related('articlecomment_set'),
            'comment_count' : ArticleComment.objects.filter(article_id=article_id).count()
        }
        return render(request, 'article_module/includes/article_comment_partial.html', context)
    return HttpResponse('response')