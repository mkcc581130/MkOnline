# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-15 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0045_auto_20171107_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxoauth',
            name='access_token',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ACCESS_TOKEN'),
        ),
        migrations.AlterField(
            model_name='wxoauth',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='REFRESH_TOKEN'),
        ),
    ]
