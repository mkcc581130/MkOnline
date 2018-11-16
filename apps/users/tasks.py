#!/usr/bin/python
# encoding:utf8

"""
@author: MK
@contact: 575151723@qq.com
@file: tasks.py
@create datetime: 18-3-26 下午4:16
"""

from __future__ import absolute_import, unicode_literals
import urllib
from celery import shared_task
from customers.models import Customer, Order, UnableCommission
from management.models import Endorsement
import datetime
from decimal import Decimal
from wechat_sdk import WechatConf, WechatBasic
from django.utils.timezone import utc


@shared_task
def download_icon(invite_id, head_img_url):
    customer = Customer.objects.get(invitation__code=invite_id)
    user_icon = 'media/customer/icon/' + invite_id + '.jpg'
    urllib.urlretrieve(head_img_url, user_icon)
    customer.user_icon = '/' + user_icon
    customer.save()


@shared_task
def auto_complete_order():
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    time = now - datetime.timedelta(days=10)
    order = Order.objects.filter(status=3)
    endorsement = Endorsement.objects.filter(id__gte=3).order_by('-id')
    conf = WechatConf(
        token='yihui8888',
        appid='wx5e1f3f920edaf478',
        appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
        encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
        encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
    )
    wechat_instance = WechatBasic(conf=conf)
    for o in order:
        if o.delivery_time <= time:
            customer = o.customers
            oid = o.oid
            goods_name = ''
            for i in o.ordergoods_set.all():
                goods_name += i.image.goods.name + ' '
            for e in endorsement:
                if customer.promote + customer.consumption >= Decimal(e.total_amount):
                    customer.classify = e
                    customer.save()
                    break
            commission = UnableCommission.objects.filter(order=o).order_by('id')
            for index in range(len(commission)):
                c = commission[index]
                spokesman = c.spokesman
                spokesman.commission += c.commission
                spokesman.enable_commission += c.commission
                spokesman.promote += c.order.paid
                if index == 0:
                    spokesman.promote += o.paid
                    spokesman.save()
                    for e in endorsement:
                        if spokesman.promote + spokesman.consumption >= Decimal(e.total_amount):
                            spokesman.classify = e
                            break
                spokesman.save()
                c.is_settled = True
                c.settled_time = now
                c.save()
                wechat_instance.send_template_message(spokesman.wxoauth.openid,
                                                      'eW13gUyvr6w8jKezE54M6uhVhe1OncZsz1I4gdgY3PU',
                                                      {
                                                          "first": {
                                                              "value": "您有一笔佣金结算成功了哦！",
                                                              "color": "#173177"},
                                                          "keyword1": {"value": customer.username, "color": "#173177"},
                                                          "keyword2": {"value": str(now.strftime('%Y年%m月%d日 %H：%M：%S')),
                                                                       "color": "#173177"},
                                                          "keyword3": {"value": "推荐客户消费提成", "color": "#173177"},
                                                          "keyword4": {"value": "佣金分成", "color": "#173177"},
                                                          "keyword5": {"value": str(c.commission), "color": "#173177"},
                                                          "remark": {"value": "如有疑问，请联系客服！", "color": "#173177"}
                                                      }, 'http://www.yihuiculture.com/endorsement/')
            o.status = 4
            o.complete_time = now
            o.save()
            wechat_instance.send_template_message(order.customers.wxoauth.openid,
                                                  'KkX496aShz9F2OW9dj9KqHDaJ4rp_qsNwE8rUzN4K5Y', {
                                                      "first": {"value": "订单已完成，欢迎您下次光临！",
                                                                "color": "#173177"},
                                                      "keyword1": {"value": oid, "color": "#173177"},
                                                      "keyword2": {"value": goods_name, "color": "#173177"},
                                                      "keyword3": {"value": str(now.strftime('%Y年%m月%d日 %H：%M：%S')),
                                                                   "color": "#173177"},
                                                      "remark": {"value": "感谢您对一慧丝绣的支持！点击查看订单详情", "color": "#C81522"}
                                                  }, 'http://www.yihuiculture.com/order_detail/' + oid)


@shared_task
def auto_close_order():
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    time = now - datetime.timedelta(minutes=10)
    order = Order.objects.filter(status=0)
    conf = WechatConf(
        token='yihui8888',
        appid='wx5e1f3f920edaf478',
        appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
        encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
        encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
    )
    wechat_instance = WechatBasic(conf=conf)
    for o in order:
        oid = o.oid
        goods_name = ''
        create_time = o.create_time
        for i in o.ordergoods_set.all():
            goods_name += i.image.goods.name + ' '
        if o.create_time <= time:
            o.status = 5
            o.complete_time = now
            o.save()
            wechat_instance.send_template_message(order.customers.wxoauth.openid,
                                                  'xXtbHaSiJgJMtnsEJMXT-fhgoQTW2C1aHnqvSmJmA_M', {
                                                      "first": {"value": "亲，您的订单已关闭",
                                                                "color": "#173177"},
                                                      "keyword1": {"value": goods_name, "color": "#173177"},
                                                      "keyword2": {"value": oid, "color": "#173177"},
                                                      "keyword3": {"value": "超时自动关闭", "color": "#173177"},
                                                      "remark": {"value": "感谢您的使用", "color": "#173177"}
                                                  })
        else:
            if not o.remind_pay:
                o.remind_pay = True
                o.save()
                wechat_instance.send_template_message(order.customers.wxoauth.openid,
                                                      '_53YqKqFPC2l8bKSb-Q86zcIFWLmW1mDdzYwWnfzlbw', {
                                                          "first": {"value": "亲，您有未支付的订单哦", "color": "#173177"},
                                                          "keyword1": {"value": goods_name, "color": "#173177"},
                                                          "keyword2": {"value": o.paid, "color": "#173177"},
                                                          "keyword3": {"value": oid, "color": "#173177"},
                                                          "keyword4": {
                                                              "value": create_time.strftime('%Y年%m月%d日 %H：%M：%S'),
                                                              "color": "#173177"},
                                                          "keyword5": {"value": (create_time + datetime.timedelta(
                                                              minutes=10)).strftime('%Y年%m月%d日 %H：%M：%S'),
                                                                       "color": "#173177"},
                                                          "remark": {"value": "订单即将逾期，点击立即支付", "color": "#C81522"}
                                                      }, 'http://www.yihuiculture.com/pay/' + oid)
