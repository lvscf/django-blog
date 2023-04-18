from django import template
from django.shortcuts import get_object_or_404
from ..models import Article, Tag, Category
from django.db.models import Count


register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_articles.html', takes_context=True)
def show_recent_articles(context, num=5):
    return {
        'recent_article_list': Article.objects.all().order_by('-create_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_dates.html', takes_context=True)
def show_dates(context):
    return {
        'date_list': Article.objects.dates('create_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_pk = get_object_or_404(Category, category='python')
    category_list = Category.objects.annotate(count=Count('article'))
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_information.html', takes_context=True)
def show_information(context, article):
    return {
        'article': article,
    }
