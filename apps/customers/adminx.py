# -*- coding: utf-8 -*-
__author__ = 'mk'
import xadmin
import datetime
from .models import Customer, WxOauth, Order, OrderGoods, Address, ReturnGoods, TransferOrders, WithdrawOrders, \
    UnableCommission, RemindOrders
from wechat_sdk import WechatConf, WechatBasic
from django.utils.timezone import utc


class WxOauthInline(object):
    model = WxOauth
    extra = 0


class OrderInline(object):
    model = Order
    extra = 0


class AddressInline(object):
    model = Address
    extra = 0


class OrderGoodsInline(object):
    model = OrderGoods
    extra = 0


class CustomerAdmin(object):
    list_display = ['username', 'tel', 'area', 'classify', 'invitation', 'get_order_num', 'consumption',
                    'promote', 'commission']
    search_fields = ['username', 'tel', 'email']
    list_filter = ['username', 'tel', 'email', 'sex', 'area', 'birthday', 'classify', 'consumption', 'promote',
                   'commission', 'red_packet', 'reg_time', 'login_time']
    readonly_fields = ['username', 'tel', 'email', 'password', 'user_icon', 'get_order_num', 'invitation', 'invited', 'consumption',
                       'promote', 'commission', 'enable_commission', 'sex', 'area', 'birthday', 'red_packet']
    list_editable = ['classify']
    inlines = [OrderInline, AddressInline, WxOauthInline]
    style_fields = {'coupon': 'm2m_transfer', 'follow': 'm2m_transfer'}


class OrderAdmin(object):
    list_display = ['oid', 'customers', 'address', 'status', 'express_num', 'delivery_time', 'paid']
    search_fields = ['oid',
                     'address__provinces__name', 'address__cities__name', 'address__areas__name', 'address__detail']
    list_filter = ['status', 'customers__username', 'paid', 'address__provinces__name', 'address__cities__name',
                   'address__areas__name', 'create_time', 'pay_time', 'delivery_time']
    list_editable = ['address', 'status', 'express_num', 'delivery_time']
    readonly_fields = ['address', 'paid']
    list_export = ('xls', 'xml', 'json')
    inlines = [OrderGoodsInline]

    def save_models(self):
        obj = self.new_obj
        status = self.model.objects.get(id=obj.id).status
        if status == 1 or status == 2:
            if obj.status == 3 and obj.express_com.name and obj.express_num:
                obj.delivery_time = datetime.datetime.utcnow().replace(tzinfo=utc)
                conf = WechatConf (
                    token='yihui8888',
                    appid='wx5e1f3f920edaf478',
                    appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                    encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
                )
                wechat_instance = WechatBasic (conf=conf)
                wechat_instance.send_template_message (obj.customers.wxoauth.openid, '-IjC-Lz5cHBS4hHqivnVHXwuej2dfu1nmfeZ8xYUJJU', {
                       "first": {"value": "店小二已为您发货，请耐心等待快递的到来哦！","color": "#173177"},
                       "keyword1": {"value": obj.oid, "color": "#173177"},
                       "keyword2": {"value": obj.express_com.name, "color": "#173177"},
                       "keyword3": {"value": str(obj.express_num), "color": "#173177"},
                       "remark": {"value": "感谢您对一慧丝绣的支持！点击查看订单详情", "color": "#173177"}
                   }, 'http://www.yihuiculture.com/order_detail/' + obj.oid)
        obj.save()


class RemindOrdersAdmin(object):
    list_display = ['order', 'remind_time']
    search_fields = ['order__oid']
    list_filter = ['order__oid', 'remind_time']
    readonly_fields = ['order', 'remind_time']


class TransferOrdersAdmin(object):
    list_display = ['oid', 'customer', 'paid', 'status', 'remark', 'transfer_time']
    search_fields = ['oid', 'customer__username']
    list_filter = ['oid', 'customer__username', 'paid', 'status', 'transfer_time']
    readonly_fields = ['oid', 'paid', 'status', 'transfer_time']


class WithdrawOrdersAdmin(object):
    list_display = ['oid', 'customer', 'name', 'account', 'bank', 'paid', 'handing_time', 'status', 'withdraw_time']
    search_fields = ['oid', 'name']
    list_filter = ['oid', 'customer__username', 'name', 'account', 'bank', 'paid', 'status', 'handing_time', 'withdraw_time']
    list_editable = ['status', 'handing_time']
    readonly_fields = ['oid', 'customer', 'name', 'account', 'bank', 'paid', 'withdraw_time']


class UnableCommissionAdmin(object):
    list_display = ['spokesman', 'order', 'commission', 'is_settled', 'settled_time']
    search_fields = ['order__oid', 'spokesman__username']
    list_filter = ['spokesman__username', 'order__customers__username', 'commission', 'is_settled', 'settled_time']
    readonly_fields = ['spokesman', 'order', 'commission', 'is_settled', 'settled_time']


class ReturnGoodsAdmin(object):
    list_display = ['order', 'refund', 'status', 'express_num', 'reason', 'apply_time', 'complete_time']
    search_fields = ['order__oid', 'customer__username', 'express_num']
    list_filter = ['status', 'refund', 'apply_time', 'complete_time']
    list_editable = ['refund', 'status', 'express_num', 'complete_time']
    list_export = ('xls', 'xml', 'json')
    style_fields = {'order_goods': 'm2m_transfer'}
# class AreaAdmin(object):
#     list_display = ['id', 'cities', 'name', 'zipcode']
#     search_fields = ['cities__name', 'name']
#     list_filter = ['cities__name', 'name', 'zipcode']
#
# xadmin.site.register(Area, AreaAdmin)
xadmin.site.register(Customer, CustomerAdmin)
xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(RemindOrders, RemindOrdersAdmin)
xadmin.site.register(TransferOrders, TransferOrdersAdmin)
xadmin.site.register(WithdrawOrders, WithdrawOrdersAdmin)
xadmin.site.register(UnableCommission, UnableCommissionAdmin)
xadmin.site.register(ReturnGoods, ReturnGoodsAdmin)
