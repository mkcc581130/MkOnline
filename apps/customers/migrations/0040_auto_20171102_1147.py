# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-02 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0039_auto_20171101_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemindOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remind_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u63d0\u9192\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u63d0\u9192\u8ba2\u5355',
                'verbose_name_plural': '\u63d0\u9192\u8ba2\u5355\u5217\u8868',
            },
        ),
        migrations.RemoveField(
            model_name='order',
            name='prepay_id',
        ),
        migrations.AddField(
            model_name='order',
            name='pay_oid',
            field=models.CharField(max_length=40, null=True, verbose_name='\u652f\u4ed8\u8ba2\u5355\u53f7'),
        ),
        migrations.AddField(
            model_name='remindorders',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Order', verbose_name='\u63d0\u9192\u8ba2\u5355'),
        ),
    ]