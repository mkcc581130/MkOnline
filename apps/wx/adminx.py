# -*- coding: utf-8 -*-
__author__ = 'mk'

from .models import WxConfig, KeyWord
import xadmin


class WxConfigAdmin(object):
    list_display = ['name', 'token', 'appid', 'appsecret', 'encrypt_mode', 'encoding_aes_key', 'access_token']
    list_editable = ['encrypt_mode',]


class KeyWordAdmin(object):
    list_display = ['keyword', 'content', 'update_time', 'published']
    list_editable = ['published', ]

xadmin.site.register(WxConfig, WxConfigAdmin)
xadmin.site.register(KeyWord, KeyWordAdmin)
