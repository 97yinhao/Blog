# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-10 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0003_auto_20190709_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='created_time',
            field=models.DateTimeField(verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='modified_time',
            field=models.DateTimeField(verbose_name='更改时间'),
        ),
    ]