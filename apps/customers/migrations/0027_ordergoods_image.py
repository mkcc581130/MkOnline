# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-04 15:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0017_auto_20170901_1958'),
        ('customers', '0026_remove_ordergoods_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordergoods',
            name='image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='goods.Images', verbose_name='\u56fe\u7247'),
        ),
    ]
