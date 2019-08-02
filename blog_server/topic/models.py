from django.db import models

# Create your models here.


class Topic(models.Model):
    title = models.CharField('题目', max_length=50)
    author = models.ForeignKey(
        'users.UserProfile',
        verbose_name='作者')
    category = models.CharField('分类', max_length=20)
    limit = models.CharField('权限', max_length=10)
    created_time = models.DateTimeField('创建时间')
    modified_time = models.DateTimeField('更改时间')
    content = models.TextField('博客内容')
    introduce = models.CharField('摘要', max_length=90)

    class Meta:
        db_table = 'topic'
