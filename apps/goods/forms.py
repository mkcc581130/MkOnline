#!/usr/bin/python
# encoding:utf8

"""
@author: MK
@contact: 575151723@qq.com
@file: forms.py
@create datetime: 17-8-10 下午4:31
"""


from django import forms
from .models import GoodsList


class GoodsListForm(forms.ModelForm):
    print 1

    class Meta:
        model = GoodsList
        exclude = ['visits']

    def clean_classify_two(self):
        classify_two = self.cleaned_data['classify_two']
        return 2
