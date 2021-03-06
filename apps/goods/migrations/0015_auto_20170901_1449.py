# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-01 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0014_auto_20170831_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_props', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.DetailProps', verbose_name='\u4e8c\u7ea7\u5c5e\u6027')),
            ],
            options={
                'verbose_name': '\u56fe\u7247\u5c5e\u6027',
                'verbose_name_plural': '\u56fe\u7247\u5c5e\u6027\u5217\u8868',
            },
        ),
        migrations.RenameModel(
            old_name='Classify',
            new_name='ClassifyList',
        ),
        migrations.AlterModelOptions(
            name='classifylist',
            options={'verbose_name': '\u5206\u7c7b', 'verbose_name_plural': '\u5206\u7c7b\u5217\u8868'},
        ),
        migrations.RemoveField(
            model_name='images',
            name='detail_props',
        ),
        migrations.AddField(
            model_name='proplist',
            name='images',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Images', verbose_name='\u56fe\u7247'),
        ),
        migrations.AddField(
            model_name='proplist',
            name='props',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Props', verbose_name='\u4e00\u7ea7\u5c5e\u6027'),
        ),
    ]
