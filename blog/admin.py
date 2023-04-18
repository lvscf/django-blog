from django.contrib import admin
from .models import Article, Tag, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'update_time', 'excerpt', 'category', 'auther']
    # fields = ['title', 'create_time', 'body', 'excerpt', 'category', 'tag']
    fields = ['title', 'body', 'excerpt', 'category', 'tag']

    def save_model(self, request, obj, form, change):
        obj.auther = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Category)
