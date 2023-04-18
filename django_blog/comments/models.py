from django.db import models
from django.utils import timezone


class Comment(models.Model):
    """
    博客的评论
    """
    name = models.CharField('名字', max_length=200)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    article = models.ForeignKey('blog.article', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-create_time', 'name']

    def __str__(self):
        return '{}:{}'.format(self.name, self.text[:20])