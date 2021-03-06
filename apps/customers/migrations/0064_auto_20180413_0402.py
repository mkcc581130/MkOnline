# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-12 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0063_auto_20180407_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='login_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u6700\u540e\u767b\u5f55\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='reg_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u6ce8\u518c\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u8ba2\u5355\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='remindorders',
            name='remind_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u63d0\u9192\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='returngoods',
            name='apply_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='withdraworders',
            name='withdraw_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u63d0\u73b0\u65f6\u95f4'),
        ),
    ]
