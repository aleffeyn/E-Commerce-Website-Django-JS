from modeltranslation.translator import TranslationOptions, register

from article_module.models import Article, ArticleCategory


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content' , 'short_description' , 'author' , 'editor')

@register(ArticleCategory)
class ArticleCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)