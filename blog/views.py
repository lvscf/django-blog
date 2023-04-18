from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def index(request):
    article_list = Article.objects.all()
    return render(request, 'blog/index.html', context={
        'article_list': article_list
    })


def dates(request, year, month):
    article_list = Article.objects.filter(create_time__year=year,
                                          create_time__month=month,
                                          ).order_by('-create_time')
    return render(request, 'blog/index.html', context={
        'article_list': article_list
    })


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    md = markdown.Markdown(extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         TocExtension(slugify=slugify)
                                     ])
    article.body = md.convert(article.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    article.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'article': article})


def category(request, pk):
    c = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=c).order_by('-create_time')
    return render(request, 'blog/index.html', context={'article_list': article_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    article_list = Article.objects.filter(tag=t).order_by('-create_time')
    return render(request, 'blog/index.html', context={'article_list': article_list})


def auther(request, pk):
    # t = get_object_or_404(Article, auther=pk)
    article_list = Article.objects.filter(auther=pk).order_by('-create_time')
    return render(request, 'blog/index.html', context={'article_list': article_list})
