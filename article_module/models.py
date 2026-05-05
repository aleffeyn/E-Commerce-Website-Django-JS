from django.core.validators import MinLengthValidator
from django.db import models
from jalali_date import date2jalali
from django.utils.translation import gettext_lazy as _

from account_module.models import User


# Create your models here.

class ArticleCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Category Name'))
    url_title = models.CharField(max_length=300, verbose_name=_('Category URL Title'), unique=True)
    is_active = models.BooleanField(verbose_name=_('Category Status'), default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'


class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/article', verbose_name='Article Image')
    category = models.ManyToManyField(ArticleCategory, verbose_name='Category')
    short_description = models.CharField(max_length=360, verbose_name='Article Short Description')
    content = models.TextField(verbose_name='Article Content')
    slug = models.SlugField(max_length=400, unique=True, db_index=True, allow_unicode=True, verbose_name='Article URL Title', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Article Status', default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author', null=True, editable=False, related_name='authored_articles')
    editor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Editor', null=True, editable=False, related_name='edited_articles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Article Created At', null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Article Updated At', null=True, editable=False)

    def __str__(self):
        return self.title

    def was_updated(self):
        """Returns True if the article was updated after creation"""
        if self.created_at and self.updated_at:
            # Allow a small time difference (1 second) to account for save operations
            from datetime import timedelta
            return self.updated_at > self.created_at + timedelta(seconds=1)
        return False

    def get_jalali_create_date(self):
        return date2jalali(self.created_at)
    def get_jalali_create_time(self):
        return self.created_at.strftime('%H:%M')
    def get_jalali_update_date(self):
        return date2jalali(self.updated_at)
    def get_jalali_update_time(self):
        return self.updated_at.strftime('%H:%M')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='Article')
    parent = models.ForeignKey('ArticleComment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Parent Comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    comment = models.TextField(verbose_name='Comment', validators=[MinLengthValidator(1, message='نظر نمیتواند خالی باشد')])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Comment Created At')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'