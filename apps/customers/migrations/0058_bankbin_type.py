# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-27 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0057_auto_20180327_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankbin',
            name='type',
            field=models.CharField(max_length=30, null=True, verbose_name='\u5361\u7c7b\u578b'),
        ),
    ]
