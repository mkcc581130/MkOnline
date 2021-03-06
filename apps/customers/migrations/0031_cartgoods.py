# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-27 15:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0019_coupon_easy_get'),
        ('customers', '0030_auto_20170927_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='\u6570\u91cf')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer', verbose_name='\u7528\u6237')),
                ('image', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='goods.Images', verbose_name='\u56fe\u7247')),
            ],
            options={
                'verbose_name': '\u8d2d\u7269\u8f66\u5546\u54c1',
                'verbose_name_plural': '\u8d2d\u7269\u8f66\u5546\u54c1\u5217\u8868',
            },
        ),
    ]
