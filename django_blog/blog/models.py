import markdown
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.urls import reverse


class Category(models.Model):
    """
    博客类别
    """
    # 类别
    category = models.CharField(max_length=100)

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category


class Tag(models.Model):
    """
    博客标签
    """
    # 标签
    tag = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Article(models.Model):
    """
    博客文章
    """
    # 标题
    title = models.CharField('标题', max_length=15)
    # 正文
    body = models.TextField('正文')
    # 创建时间
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    # 修改时间
    update_time = models.DateTimeField('更新时间')
    # 摘要
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    # 类别
    category = models.ForeignKey(Category, verbose_name='类别', on_delete=models.CASCADE)
    # 标签
    tag = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 作者
    auther = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_time', 'title']

    def save(self, *args, **kwargs):
        self.update_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
