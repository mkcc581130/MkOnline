# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-31 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0012_auto_20170831_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='classify_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.ClassifyTwo', verbose_name='\u4e8c\u7ea7\u5206\u7c7b'),
        ),
    ]
