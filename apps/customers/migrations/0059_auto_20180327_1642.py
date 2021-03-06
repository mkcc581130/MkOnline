# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-27 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0058_bankbin_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdraworders',
            name='account',
            field=models.CharField(max_length=20, null=True, verbose_name='\u94f6\u884c\u8d26\u53f7'),
        ),
        migrations.AddField(
            model_name='withdraworders',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.BankBin', verbose_name='\u6240\u5c5e\u94f6\u884c'),
        ),
        migrations.AddField(
            model_name='withdraworders',
            name='handing_time',
            field=models.DateTimeField(null=True, verbose_name='\u63d0\u73b0\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='bankbin',
            name='bank',
            field=models.CharField(max_length=30, null=True, verbose_name='\u94f6\u884c\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='bankbin',
            name='bin',
            field=models.CharField(max_length=20, null=True, verbose_name='bin'),
        ),
        migrations.AlterField(
            model_name='withdraworders',
            name='paid',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u63d0\u73b0\u91d1\u989d'),
        ),
        migrations.AlterField(
            model_name='withdraworders',
            name='status',
            field=models.IntegerField(choices=[(0, '\u672a\u5904\u7406'), (1, '\u5df2\u5904\u7406')], default=0, verbose_name='\u72b6\u6001'),
        ),
    ]
