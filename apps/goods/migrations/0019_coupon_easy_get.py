# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-19 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0018_express'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='easy_get',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u80fd\u9886\u53d6'),
        ),
    ]
