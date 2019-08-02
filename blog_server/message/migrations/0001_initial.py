# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-11 08:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('topic', '0004_auto_20190710_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=60, verbose_name='留言内容')),
                ('created_time', models.DateTimeField(verbose_name='创建时间')),
                ('parent_message', models.IntegerField(verbose_name='父留言ID')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topic.Topic')),
            ],
            options={
                'db_table': 'message',
            },
        ),
    ]
