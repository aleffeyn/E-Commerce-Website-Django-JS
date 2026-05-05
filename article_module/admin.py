from django.contrib import admin

from article_module.models import Article, ArticleCategory, ArticleComment


# Register your models here.
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active', 'parent']
    list_editable = ['parent','is_active']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','slug', 'is_active', 'author', 'editor']
    list_editable = ['is_active']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        else:
            obj.editor = request.user
        return super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'user' , 'parent' , 'created_at']

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, CommentAdmin)
