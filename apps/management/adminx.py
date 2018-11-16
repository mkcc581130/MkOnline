# -*- coding: utf-8 -*-
__author__ = 'mk'
import xadmin
from .models import Banner, Verify, Endorsement, NormalQuestion, RedPacket


class BannerAdmin(object):
    list_display = ['title', 'img', 'index', 'url', 'add_time']
    search_fields = ['title']
    list_filter = ['title', 'index', 'add_time']
    readonly_fields = ['add_time']
    list_editable = ['title', 'index', 'url']


class VerifyAdmin (object):
    list_display = ['tel', 'code', 'create_time']
    search_fields = ['tel']
    list_filter = ['tel', 'code', 'create_time']
    readonly_fields = ['create_time']


class EndorsementAdmin(object):
    list_display = ['name', 'get_customer_num', 'total_amount', 'first_commission', 'second_commission', 'third_commission', 'discount']
    search_fields = ['name']
    list_filter = ['name', 'create_time']
    readonly_fields = ['create_time']
    list_editable = ['total_amount', 'first_commission', 'second_commission', 'third_commission', 'discount']


class NormalQuestionAdmin(object):
    list_display = ['title', 'sort', 'create_time', 'modify_time']
    search_fields = ['title']
    list_filter = ['title', 'sort', 'create_time', 'modify_time']
    readonly_fields = ['create_time']
    list_editable = ['title', 'sort', 'modify_time']
    style_fields = {"content": "ueditor"}


class RedPacketAdmin (object):
    list_display = ['money', 'rate', 'min_paid', 'enable']
    list_filter = ['money', 'rate', 'min_paid', 'enable']
    list_editable = ['money', 'rate', 'min_paid', 'enable']


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Verify, VerifyAdmin)
xadmin.site.register(Endorsement, EndorsementAdmin)
xadmin.site.register(NormalQuestion, NormalQuestionAdmin)
xadmin.site.register(RedPacket, RedPacketAdmin)
