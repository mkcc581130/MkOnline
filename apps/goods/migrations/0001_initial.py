# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-09 10:11
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brands', models.CharField(max_length=30, verbose_name='\u54c1\u724c')),
            ],
            options={
                'verbose_name': '\u54c1\u724c\u5217\u8868',
                'verbose_name_plural': '\u54c1\u724c\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='ClassifyOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u540d\u79f0')),
                ('en_name', models.CharField(max_length=20, verbose_name='Name')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b\u5217\u8868',
                'verbose_name_plural': '\u5206\u7c7b\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='ClassifyTwo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u540d\u79f0')),
                ('en_name', models.CharField(max_length=20, verbose_name='Name')),
                ('classify_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ClassifyOne', verbose_name='\u4e00\u7ea7\u5206\u7c7b')),
            ],
            options={
                'verbose_name': '\u4e8c\u7ea7\u5206\u7c7b',
                'verbose_name_plural': '\u4e8c\u7ea7\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='DetailProps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='\u540d\u79f0')),
                ('en_name', models.CharField(default='', max_length=20, verbose_name='Name')),
            ],
            options={
                'verbose_name': '\u4e8c\u7ea7\u5c5e\u6027',
                'verbose_name_plural': '\u4e8c\u7ea7\u5c5e\u6027',
            },
        ),
        migrations.CreateModel(
            name='ExtraImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='goods/image/extra/', verbose_name='\u56fe\u7247')),
            ],
            options={
                'verbose_name': '\u989d\u5916\u56fe\u7247\u5217\u8868',
                'verbose_name_plural': '\u989d\u5916\u56fe\u7247\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='GoodsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u5546\u54c1\u540d\u79f0')),
                ('en_name', models.CharField(max_length=50, verbose_name='Goods Name')),
                ('gid', models.CharField(max_length=20, verbose_name='\u5546\u54c1\u7f16\u53f7')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5546\u54c1\u4ef7\u683c')),
                ('dis_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u6298\u6263\u4ef7\u683c')),
                ('integral', models.IntegerField(verbose_name='\u5546\u54c1\u79ef\u5206')),
                ('to_front', models.BooleanField(default=True, verbose_name='\u4e0a\u4e0b\u67b6')),
                ('sort', models.IntegerField(verbose_name='\u5546\u54c1\u6392\u5e8f')),
                ('intr', models.TextField(verbose_name='\u5546\u54c1\u7b80\u4ecb')),
                ('detail', DjangoUeditor.models.UEditorField(default='', verbose_name='\u5546\u54c1\u8be6\u60c5')),
                ('endetail', DjangoUeditor.models.UEditorField(default='', verbose_name='\u5546\u54c1\u8be6\u60c5\uff08\u82f1\u6587\uff09')),
                ('en_intr', models.TextField(verbose_name='Goods Intr')),
                ('visits', models.IntegerField(default=0, verbose_name='\u6d4f\u89c8\u91cf')),
                ('counts', models.IntegerField(default=0, verbose_name='\u9500\u552e\u91cf')),
                ('is_new', models.BooleanField(default=False, verbose_name='\u65b0\u54c1\u4e0a\u5e02')),
                ('is_hot', models.BooleanField(default=False, verbose_name='\u70ed\u5356\u5546\u54c1')),
                ('is_ex', models.BooleanField(default=False, verbose_name='\u7cbe\u9009\u5546\u54c1')),
                ('to_front_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u4e0a\u67b6\u65f6\u95f4')),
                ('brands', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Brand', verbose_name='\u54c1\u724c')),
            ],
            options={
                'verbose_name': '\u5546\u54c1\u5217\u8868',
                'verbose_name_plural': '\u5546\u54c1\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='goods/image/', verbose_name='\u56fe\u7247')),
                ('stocks', models.CharField(default='1', max_length=100, verbose_name='\u5e93\u5b58\u91cf')),
                ('detail_props', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.DetailProps', verbose_name='\u4e8c\u7ea7\u5c5e\u6027')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsList', verbose_name='\u5546\u54c1')),
            ],
            options={
                'verbose_name': '\u56fe\u7247\u5217\u8868',
                'verbose_name_plural': '\u56fe\u7247\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Props',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='\u540d\u79f0')),
                ('en_name', models.CharField(default='', max_length=20, verbose_name='Name')),
            ],
            options={
                'verbose_name': '\u5c5e\u6027\u5217\u8868',
                'verbose_name_plural': '\u5c5e\u6027\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Visit_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6d4f\u89c8\u65f6\u95f4')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsList', verbose_name='\u5546\u54c1')),
            ],
            options={
                'verbose_name': '\u6d4f\u89c8\u91cf',
                'verbose_name_plural': '\u6d4f\u89c8\u91cf',
            },
        ),
        migrations.AddField(
            model_name='extraimages',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsList', verbose_name='\u5546\u54c1'),
        ),
        migrations.AddField(
            model_name='detailprops',
            name='props',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Props', verbose_name='\u4e0a\u7ea7\u5c5e\u6027'),
        ),
    ]
