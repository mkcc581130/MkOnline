# coding:utf-8
from django import template
from decimal import *
register = template.Library()


def dec_price(data):
    data = str(data)
    return data[data.find(unicode(".", "utf-8")):]
register.filter(dec_price)


def int_price(data):
    data = str(data)
    return data[0:data.find(unicode(".", "utf-8"))]
register.filter(int_price)


def discount(data):
    num = ('零', '一', '二', '三', '四', '五', '六', '七', '八', '九')
    if data % 10 == 0:
        return num[data/10]
    else:
        return num[data/10] + num[data % 10]
register.filter(discount)
