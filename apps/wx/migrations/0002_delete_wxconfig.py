# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-25 19:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wx', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WxConfig',
        ),
    ]
