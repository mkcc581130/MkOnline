# -*- coding: utf-8 -*-
__author__ = 'mk'
import xadmin
from .models import GoodsList, ClassifyTwo, ClassifyOne, Props, DetailProps, Images, ExtraImages, Brand, Coupon, ClassifyList, PropList
from .forms import GoodsListForm


class PropInline(object):
    model = PropList
    extra = 0


class ImagesInline(object):
    model = Images
    extra = 0


class ClassifyInline(object):
    model = ClassifyList
    extra = 0


class ExtraImagesInline(object):
    model = ExtraImages
    extra = 0


class ClassifyTwoInline(object):
    model = ClassifyTwo
    extra = 0


class DetailPropsInline(object):
    model = DetailProps
    extra = 0


class GoodsAdmin(object):
    list_display = ['name', 'img_tag', 'price', 'gid', 'to_front', 'counts', 'visits']
    search_fields = ['name', 'gid', 'en_name']
    list_filter = ['name', 'gid', 'en_name', 'have_commission', 'price', 'to_front', 'counts', 'visits', 'is_new', 'is_hot', 'is_ex',
                   'to_front_time']
    readonly_fields = ['to_front_time', 'modify_time', 'counts', 'visits']
    list_editable = ['price', 'gid', 'have_commission', 'to_front']
    list_export = ('xls', 'json')
    inlines = [ClassifyInline, ImagesInline, ExtraImagesInline]
    style_fields = {"detail": "ueditor", "endetail": "ueditor"}
    form = GoodsListForm
# class ClassifyTwoAdmin(object):
#     list_display = ['name', 'en_name', 'classify_one', 'get_goods_num']
#     search_fields = ['name', 'en_name']
#     list_filter = ['name', 'en_name', 'classify_one']
#


class ClassifyOneAdmin(object):
    list_display = ['name', 'img_tag', 'get_ct_num']
    search_fields = ['name', 'en_name']
    list_filter = ['name', 'en_name']
    list_editable = ['name']
    inlines = [ClassifyTwoInline]


class PropsAdmin(object):
    list_display = ['name', 'en_name', 'get_dp_num']
    search_fields = ['name', 'en_name']
    list_filter = ['name', 'en_name']
    inlines = [DetailPropsInline]

# class DetailPropsAdmin(object):
#     list_display = ['name', 'en_name']
#     search_fields = ['name', 'en_name']
#     list_filter = ['name', 'en_name']


class ImagesAdmin(object):
    list_display = ['goods', 'img_tag', 'stocks', 'stocks_ht', 'backstage_props']
    search_fields = ['goods__name', 'goods__en_name']
    list_filter = ['goods__name', 'stocks', 'stocks_ht']
    list_editable = ['stocks', 'stocks_ht']
    inlines = [PropInline]


class BrandAdmin(object):
    list_display = ['name', 'get_goods']
    search_fields = ['name']
    list_filter = ['name']


class CouponAdmin(object):
    list_display = ['name', 'goods', 'full', 'dis', 'is_auto', 'easy_get', 'start_time', 'end_time']
    search_fields = ['name', 'goods__name']
    list_filter = ['full', 'dis', 'is_auto', 'easy_get', 'start_time', 'end_time']
    list_editable = ['name', 'full', 'dis', 'is_auto', 'easy_get', 'start_time', 'end_time']
    style_fields = {'goods': 'm2m_transfer'}

xadmin.site.register(GoodsList, GoodsAdmin)
xadmin.site.register(ClassifyOne, ClassifyOneAdmin)
# xadmin.site.register(ClassifyTwo, ClassifyTwoAdmin)
xadmin.site.register(Props, PropsAdmin)
xadmin.site.register(Brand, BrandAdmin)
xadmin.site.register(Coupon, CouponAdmin)
xadmin.site.register(Images, ImagesAdmin)
# xadmin.site.register(DetailProps, DetailPropsAdmin)
# xadmin.site.register(Images, ImagesAdmin)

