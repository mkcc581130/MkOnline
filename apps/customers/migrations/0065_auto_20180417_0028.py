# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-16 16:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0064_auto_20180413_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.City', verbose_name='\u6240\u5728\u57ce\u5e02'),
        ),
        migrations.AddField(
            model_name='customer',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='\u51fa\u751f\u5e74\u6708'),
        ),
        migrations.AddField(
            model_name='customer',
            name='sex',
            field=models.IntegerField(blank=True, choices=[(1, '\u7537'), (2, '\u5973')], null=True, verbose_name='\u6027\u522b'),
        ),
        migrations.AddField(
            model_name='order',
            name='remind_pay',
            field=models.BooleanField(default=False, verbose_name='\u63d0\u9192\u652f\u4ed8'),
        ),
    ]
