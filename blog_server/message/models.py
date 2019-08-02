from django.db import models

# Create your models here.


class Message(models.Model):
    topic = models.ForeignKey('topic.Topic')
    content = models.CharField('留言内容', max_length=60)
    created_time = models.DateTimeField('创建时间')
    parent_message = models.IntegerField('父留言ID')
    publisher = models.ForeignKey('users.UserProfile')

    class Meta:
        db_table = 'message'
