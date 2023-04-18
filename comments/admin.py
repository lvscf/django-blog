from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'text', 'create_time', 'article']
    fields = ['name', 'email', 'url', 'text', 'article']


admin.site.register(Comment, CommentAdmin)
# admin.site.register(Comment)
