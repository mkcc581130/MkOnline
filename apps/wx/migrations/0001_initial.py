# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-23 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WxConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=20, verbose_name='Token')),
                ('appid', models.CharField(max_length=40, verbose_name='\u5e94\u7528ID')),
                ('appsecret', models.CharField(max_length=40, verbose_name='\u5e94\u7528secret')),
                ('encrypt_mode', models.CharField(choices=[('normal', '\u660e\u6587'), ('compatible', '\u517c\u5bb9'), ('safe', '\u5b89\u5168')], max_length=15)),
                ('encoding_aes_key', models.CharField(max_length=40, verbose_name='\u6d88\u606f\u52a0\u5bc6\u5bc6\u94a5')),
            ],
        ),
    ]
