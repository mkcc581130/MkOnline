# _*_ encoding:utf-8 _*_
import json
import os
import tasks
import pytz
import express
import time
import random
import re
import qrcode
from decimal import *
from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from .forms import FindPwdForm
from customers.models import Customer, WxOauth, Address, Province, City, Area, Order, OrderGoods, CartGoods, \
    RemindOrders, TransferOrders, Invitation, UnableCommission, BankBin, WithdrawOrders
from management.models import Banner, Verify, Endorsement, NormalQuestion, RedPacket
from sms import Sms
from goods.models import Coupon, GoodsList, ClassifyOne, PropList, Images
from django.core import serializers
from PIL import Image
from wx.models import WxConfig
from wechat_sdk import WechatOauth, WeChatPay, WechatConf, WechatBasic
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from django.utils.timezone import utc

domain_name = "http://101.132.38.60/"


class Authenticate(object):
    def __init__(self, request):
        self.request = request

    """
        判断用户是否已经登录。
    """
    @property
    def is_active(self):
        if 'username' in self.request.session:
            username = self.request.session['username']  # session中用户名
            # 判断用户是否存在
            try:
                customer = Customer.objects.get(Q(email=username) | Q(tel=username))
                password = self.request.session['password']
                if check_password(password, customer.password):
                    return True
                elif password == customer.password:
                    return True
                else:
                    return False
            except Customer.DoesNotExist:
                try:
                    Customer.objects.get(wxoauth__openid=username)
                    return True
                except Customer.DoesNotExist:
                    return False
        else:
            return False


class InvitationManage(object):
    def __init__(self, invite_id=None, **kwargs):
        if invite_id:
            self.invite_id = invite_id
        else:
            self.invite_id = self.get_invite_id()
        s = ''
        if kwargs:
            s = "_".join(["%s_%s" % (key, value) for key, value in kwargs])
        self.qr_path = 'media/customer/qr_invitation/%s_%s.png' % (invite_id, s)  # 二维码图片路径
        self.path = 'media/customer/invitation/%s_%s.png' % (invite_id, s)  # 推荐图图片路径

    """
        当用户没有推荐码时，获取推荐码！
    """
    @staticmethod
    def get_invite_id():
        after_time = "%s%s" % (str(random.randint(1, 9)), str(int(time.time() * 10) - 15000609000))
        invite_id = ''
        letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']
        for i in range(0, 10, 2):
            num = int(after_time[i:i + 2])
            if num <= 25:
                invite_id += letter[num - 1]
            else:
                invite_id += letter[int(after_time[i:i + 1])] + after_time[i + 1:i + 2]
        invite_id += after_time[10:]
        return invite_id

    """
        获取二维码图
    """
    def get_qrcode(self, request):
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8)
        qr.add_data('http://%s%s?invitation=%s' % (request.get_host(), request.path, self.invite_id))
        qr.make(fit=True)
        img = qr.make_image()
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = img.convert("RGBA")
        img.save(self.qr_path)
        return img

    """
        获取包含二维码的推荐图
    """
    def get_invite_img(self, request, icon_url):
        img = self.get_qrcode(request)
        bg = Image.open('media/customer/invitation/invite_bg.jpg').convert("RGBA")
        icon = Image.open(icon_url)
        icon = icon.resize((128, 128), Image.ANTIALIAS)
        icon = icon.convert("RGBA")
        bg.paste(icon, (60, 840))
        bg.paste(img, (480, 850))
        bg = bg.resize((360, 559), Image.ANTIALIAS)
        bg.save(self.path)


class IndexView(View):
    # 首页视图
    @staticmethod
    def get(request):
        request.session['login_back'] = request.build_absolute_uri()
        if 'first' not in request.session:
            request.session['first'] = 'welcome'
            return redirect('index')
        banners = Banner.objects.all().order_by('index')  # 轮播图
        new_goods = GoodsList.objects.filter(Q(is_new=True) & Q(to_front=True)).order_by('-sort')  # 新品
        hot_goods = GoodsList.objects.filter(Q(is_hot=True) & Q(to_front=True)).order_by('-sort')  # 热卖商品
        ex_goods = GoodsList.objects.filter(Q(is_ex=True) & Q(to_front=True)).order_by('-sort')  # 精选商品
        dis_goods = GoodsList.objects.filter(Q(is_dis=True) & Q(to_front=True)).order_by('-sort')  # 限时折扣商品
        # 截取一定数量的商品列表
        new_goods = (len(new_goods) > 6) and new_goods[:6] or new_goods
        hot_goods = (len(hot_goods) > 6) and hot_goods[:6] or hot_goods
        ex_goods = (len(ex_goods) > 6) and ex_goods[:6] or ex_goods
        dis_goods = (len(dis_goods) > 10) and dis_goods[:10] or dis_goods
        active = Authenticate(request).is_active
        if active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            cart_len = len(CartGoods.objects.filter(Q(single=False) & Q(customer=customer)))  # 购物车商品数量
        else:
            # 未登录时，购物车商品数量
            cart_len = len(CartGoods.objects.filter(anonymous=request.COOKIES['sessionid']))
        return render(request, 'index.html', {
            'is_active': active,
            'banners': banners,
            'new': new_goods,
            'hot': hot_goods,
            'ex': ex_goods,
            'dis': dis_goods,
            'len': cart_len
        })


class DetailView(View):
    # 商品详情视图
    @staticmethod
    def get(request, gid):
        # 判断是否有商品id参数
        if gid:
            request.session['login_back'] = request.build_absolute_uri()  # 设置登录回调session参数
            # 判断是否有微信的code参数
            if "code" in request.GET:
                wx_config = WxConfig.objects.get(id=1)  # 数据库微信参数
                wx_oauth = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret)  # 微信登录实例
                fetch_access_token = wx_oauth.fetch_access_token(code=request.GET['code'])  # 获取access_token
                try:
                    # 更新access_token, refresh_token
                    wx_oauth_obj = WxOauth.objects.get(openid=fetch_access_token['openid'])
                    wx_oauth_obj.access_token = fetch_access_token['access_token']
                    wx_oauth_obj.refresh_token = fetch_access_token['refresh_token']
                    wx_oauth_obj.save()
                except WxOauth.DoesNotExist:
                    # 不存在微信登录信息，获取用户微信信息
                    user_info = wx_oauth.get_user_info()
                    invite_id = InvitationManage().get_invite_id()
                    user_icon = '/media/customer/icon/newDefault.png'
                    invitation = Invitation(code=invite_id)
                    invitation.save()
                    # 判断是否有推荐人
                    if not request.GET['state'] == '0':
                        # 生成用户数据
                        customer = Customer(username=user_info['nickname'].encode('iso8859-1'), classify_id=2,
                                            user_icon=user_icon, invitation=invitation,
                                            invited=Invitation.objects.get(code=request.GET['state']),
                                            last_ip=request.META['REMOTE_ADDR'])
                    else:
                        customer = Customer(username=user_info['nickname'].encode('iso8859-1'),
                                            user_icon=user_icon, invitation=invitation,
                                            last_ip=request.META['REMOTE_ADDR'])
                    customer.save()
                    # 生成用户微信数据并保存
                    WxOauth(customer=customer, openid=fetch_access_token['openid'],
                            access_token=fetch_access_token['access_token'],
                            refresh_token=fetch_access_token['refresh_token']).save()
                    # 延时下载用户头像，加快登录速度
                    if user_info['headimgurl']:
                        tasks.download_icon.delay(invite_id, user_info['headimgurl'])
                request.session['username'] = fetch_access_token['openid']  # 设置session用户
                return redirect('detail', gid)
            # 获取商品库存
            elif 'img_id' in request.GET:
                return JsonResponse({'stocks': Images.objects.get(id=request.GET['img_id']).get_stocks()})

            goods = GoodsList.objects.get(id=gid)
            is_active = Authenticate(request).is_active
            content = {}
            if is_active:
                username = request.session['username']
                customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                address = Address.objects.filter(Q(default=True) & Q(customers=customer))
                if 'invitation' in request.GET:
                    conf = WechatConf(
                        token='yihui8888',
                        appid='wx5e1f3f920edaf478',
                        appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                        encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                        encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
                    )
                    wechat_instance = WechatBasic(conf=conf)
                    invite_id = customer.invitation.code
                    scene_str = {
                        'iid': invite_id,
                        'gid': gid
                    }
                    scene_str = json.dumps(scene_str)
                    dic = wechat_instance.create_qrcode({"expire_seconds": 2592000, "action_name": "QR_STR_SCENE",
                                                         "action_info": {"scene": {"scene_str": scene_str}}})
                    return redirect(dic['url'])
                # 获取二维码，推荐图
                if 'img' in request.GET:
                    im = InvitationManage(invite_id=customer.invitation.code, goods_id=gid)
                    if request.GET['img'] == 'qrcode':
                        qr_path = im.qr_path
                        if not os.path.exists(qr_path):
                            im.get_qrcode(request)
                        return JsonResponse({'img_url': '/%s' % qr_path})
                    elif request.GET['img'] == 'tuwen':
                        path = im.path
                        if not os.path.exists(path):
                            im.get_invite_img(request, str(customer.user_icon.url)[7:])
                    else:
                        path = ''
                    return JsonResponse({'img_url': '/%s' % path})
                # 商品加入收藏
                elif 'follow' in request.GET:
                    username = request.session['username']
                    customer = Customer.objects.get(
                        Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                    follow = GoodsList.objects.filter(customer=customer)
                    if goods in follow:
                        customer.follow.remove(goods)
                    else:
                        customer.follow.add(goods)
                    return JsonResponse({'success': True})
                # 判断用户是否为代言人，享受折扣大小
                if customer.classify_id != 1:
                    content['dis_price'] = goods.price * customer.classify.discount / 100
                    content['promote'] = "%.2f" % (goods.price * customer.classify.first_commission / 100)
                # 获取地址
                if address:
                    content['address'] = address[0]
                content['len'] = len(CartGoods.objects.filter(Q(customer=customer) & Q(single=False)))
                follow = GoodsList.objects.filter(customer=customer)
                content['follow'] = goods in follow
                # 判断是否为微信
                if 'is_wx' in content:
                    content['iid'] = customer.invitation.code
            else:
                content['len'] = len(CartGoods.objects.filter(anonymous=request.COOKIES['sessionid']))
            # 页面尾部商品
            ex_goods = GoodsList.objects.filter(Q(is_ex=True) & Q(to_front=True)).order_by('-sort')
            ex_goods = (len(ex_goods) > 10) and ex_goods[:10] or ex_goods
            content.update({
                'is_active': is_active,
                'goods': goods,
                'ex': ex_goods,
            })
            # 是否上架
            if goods.to_front and goods.get_imgs():
                content['to_front'] = True
            # 是否为微信客户端
            if re.search("MicroMessenger", request.META['HTTP_USER_AGENT']):
                content['is_wx'] = True
                conf = WechatConf(
                    token='yihui8888',
                    appid='wx5e1f3f920edaf478',
                    appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                    encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
                )
                wechat_instance = WechatBasic(conf=conf)
                content['appid'] = 'wx5e1f3f920edaf478'
                content['timestamp'] = int(time.time())
                content['noncestr'] = random.randrange(1000000000, 2000000000)
                content['signature'] = wechat_instance.generate_jsapi_signature(timestamp=content['timestamp'],
                                                                                noncestr=content['noncestr'],
                                                                                url=request.build_absolute_uri())
            return render(request, 'detail.html', content)
        else:
            return redirect('index')

    @staticmethod
    def post(request, gid):
        if 'method' in request.POST:
            # 加入购物车
            if request.POST['method'] == 'add':
                if Authenticate(request).is_active:
                    username = request.session['username']
                    customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                    img_id = request.POST['img_id']
                    number = request.POST['number']
                    try:
                        cart_goods = CartGoods.objects.get(Q(image_id=img_id) & Q(customer=customer) & Q(single=False))
                        cart_goods.number += int(number)
                        cart_goods.save()
                    except CartGoods.DoesNotExist:
                        CartGoods(customer=customer, image_id=img_id, number=number).save()
                    cart_len = len(CartGoods.objects.filter(Q(customer=customer) & Q(single=False)))
                else:
                    CartGoods(anonymous=request.COOKIES['sessionid'], image_id=request.POST['img_id'],
                              number=request.POST['number']).save()
                    cart_len = len(CartGoods.objects.filter(anonymous=request.COOKIES['sessionid']))
                return JsonResponse({'gid': gid, 'msg': 'success', 'len': cart_len})


class DifferView(View):
    # 商品分类视图
    @staticmethod
    def get(request):
        if 'cid' in request.GET:
            goods_list = []
            goods = GoodsList.objects.filter(
                Q(classifylist__classify_one_id=request.GET['cid']) & Q(to_front=True)).order_by('-sort')
            for g in goods:
                goods_list.append({'id': g.id, 'name': g.name, 'price': g.price,
                                   'img': '/media/%s' % str(Images.objects.filter(goods=g)[0].src)})
            return JsonResponse({'goods': goods_list})
        else:
            classify = []
            classify_all = ClassifyOne.objects.filter(id__gte=11)
            for c in classify_all:
                classify.append({
                    'classify_one': c,
                    'classify_two': c.classifytwo_set.all().order_by('-sort')
                })
            return render(request, 'differ.html', {
                'classify': classify
            })


class MoreView(View):
    # 商品列表通用视图
    @staticmethod
    def get(request, way):
        if way == 'new':
            goods = GoodsList.objects.filter(is_new=True)
            title = '新品列表'
        elif way == 'hot':
            goods = GoodsList.objects.filter(is_hot=True)
            title = '热门商品列表'
        elif way == 'ex':
            goods = GoodsList.objects.filter(is_ex=True)
            title = '精选商品列表'
        elif Authenticate(request).is_active:
            if way == 'follow':
                username = request.session['username']
                goods = GoodsList.objects.filter(Q(customer__tel=username) | Q(customer__email=username) |
                                                 Q(customer__wxoauth__openid=username))
                title = '关注商品列表'
            elif way[0:6] == 'coupon':
                goods = GoodsList.objects.filter(coupon__id=way[6:])
                title = '优惠券商品列表'
            elif way == 'promote':
                goods = GoodsList.objects.filter(have_commission=True)
                title = '可推广商品列表'
            else:
                return redirect('index')
        else:
            return redirect('index')
        return render(request, 'more.html', {
            'goods': goods.filter(to_front=True).order_by('-sort'),
            'title': title
        })


class SearchView(View):
    # 搜索结果视图
    @staticmethod
    def get(request):
        if 'search' in request.GET:
            search = request.GET.get('search', '')
            goods = GoodsList.objects.filter(Q(name__icontains=search) | Q(en_name__icontains=search))
            prop_list = PropList.objects.filter(
                Q(detail_props__name__icontains=search) | Q(detail_props__en_name__icontains=search))
            for p in prop_list:
                goods = goods | GoodsList.objects.filter(images__proplist=p)
            goods = goods.distinct().filter(to_front=True).order_by('-sort')
            return render(request, 'search.html', {
                'goods': goods,
                'search': search
            })
        if 'cid' in request.GET:
            goods = GoodsList.objects.filter(
                Q(classifylist__classify_two__id=request.GET.get('cid', '')) & Q(to_front=True))
            return render(request, 'search.html', {
                'goods': goods,
                'search': ''
            })
        else:
            return redirect('index')


class TelView(View):
    # 手机号设置视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            # 获取验证码
            if "tel" in request.GET:
                tel = request.GET['tel']
                if Customer.objects.filter(tel=tel):
                    return JsonResponse({'msg': '该手机号已被注册,请直接登录！'})
                sms_status = Sms().send_sms(tel, '一慧文创馆', 'SMS_129760130')
                if sms_status:
                    return JsonResponse({'msg': 'success'})
                else:
                    return JsonResponse({'msg': '该手机号获取过于频繁，请稍后重试！'})
            username = request.session['username']
            c = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            return render(request, "tel.html", {"tel": c.tel})
        else:
            return redirect('login')

    @staticmethod
    def post(request):
        # 按钮提交
        if Authenticate(request).is_active:
            username = request.session['username']
            c = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            tel = request.POST['tel']
            verify = request.POST['verify']
            password = request.POST['password']
            if Customer.objects.filter(tel=tel):
                return JsonResponse({'msg': '该手机号已被注册,请直接登录！'})
            else:
                try:
                    ver = Verify.objects.get(tel=tel).code
                    if verify != ver:
                        return JsonResponse({'msg': '验证码错误,请重新输入！'})
                except Verify.DoesNotExist:
                    return JsonResponse({'msg': '验证码不存在,请重新获取！'})
            Verify.objects.filter(tel=tel).delete()
            c.tel = tel
            c.password = make_password(password)
            c.save()
            return JsonResponse({'msg': 'success'})


class RegisterView(View):
    # 注册视图
    @staticmethod
    def get(request):
        if "tel" in request.GET:
            tel = request.GET['tel']
            if Customer.objects.filter(tel=tel):
                return JsonResponse({'msg': '该手机号已被注册,请直接登录！'})
            sms_status = Sms().send_sms(tel, '一慧文创馆', 'SMS_90015014')
            if sms_status:
                return JsonResponse({'msg': 'success'})
            else:
                return JsonResponse({'msg': '该手机号获取过于频繁，请稍后重试！'})
        return render(request, "reg.html", {"is_active": Authenticate(request).is_active})

    @staticmethod
    def post(request):
        # 按钮提交
        tel = request.POST['tel']
        verify = request.POST['verify']
        password = request.POST['password']
        if Customer.objects.filter(tel=tel):
            return JsonResponse({'msg': '该手机号已被注册,请直接登录！'})
        else:
            try:
                ver = Verify.objects.get(tel=tel).code
                if verify != ver:
                    return JsonResponse({'msg': '验证码错误,请重新输入！'})
            except Verify.DoesNotExist:
                return JsonResponse({'msg': '验证码不存在,请重新获取！'})
        Verify.objects.filter(tel=tel).delete()
        request.session['username'] = tel
        request.session['password'] = password
        invite_id = InvitationManage().get_invite_id()
        invitation = Invitation(code=invite_id)
        invitation.save()
        # 判断是否有推荐人
        if 'iid' in request.GET:
            customer = Customer(username="一慧会员%s" % tel, tel=tel, password=make_password(password),
                                invitation=invitation, classify_id=2,
                                invited=Invitation.objects.get(code=request.GET['iid']),
                                last_ip=request.META['REMOTE_ADDR'])
        else:
            customer = Customer(username="一慧会员%s" % tel, tel=tel, password=make_password(password),
                                invitation=invitation, last_ip=request.META['REMOTE_ADDR'])
        customer.save()
        return JsonResponse({'msg': 'success'})


class LoginView(View):
    # 登录视图
    @staticmethod
    def get(request):
        # 获取验证码
        if "tel" in request.GET:
            tel = request.GET['tel']
            if not Customer.objects.filter(tel=tel):
                return JsonResponse({'msg': '该手机号未注册，请点击注册！'})
            sms_status = Sms().send_sms(tel, '一慧文创馆', 'SMS_88980025')
            if sms_status:
                return JsonResponse({'msg': 'success'})
            else:
                return JsonResponse({'msg': '该手机号获取过于频繁，请稍后重试！'})
        # 微信登录
        elif "code" in request.GET:
            wx_config = WxConfig.objects.get(id=1)
            wx_oauth = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret)
            fetch_access_token = wx_oauth.fetch_access_token(code=request.GET['code'])
            try:
                wx_oauth_obj = WxOauth.objects.get(openid=fetch_access_token['openid'])
                wx_oauth_obj.access_token = fetch_access_token['access_token']
                wx_oauth_obj.refresh_token = fetch_access_token['refresh_token']
                wx_oauth_obj.save()
            except WxOauth.DoesNotExist:
                user_info = wx_oauth.get_user_info()
                invite_id = InvitationManage().get_invite_id()
                user_icon = '/media/customer/icon/newDefault.png'
                invitation = Invitation(code=invite_id)
                invitation.save()
                if not request.GET['state'] == '0':
                    customer = Customer(username=user_info['nickname'].encode('iso8859-1'), classify_id=2,
                                        user_icon=user_icon, invitation=invitation,
                                        invited=Invitation.objects.get(code=request.GET['state']),
                                        last_ip=request.META['REMOTE_ADDR'])
                else:
                    customer = Customer(username=user_info['nickname'].encode('iso8859-1'),
                                        user_icon=user_icon, invitation=invitation,
                                        last_ip=request.META['REMOTE_ADDR'])
                customer.save()
                WxOauth(customer=customer, openid=fetch_access_token['openid'],
                        access_token=fetch_access_token['access_token'],
                        refresh_token=fetch_access_token['refresh_token']).save()
                if user_info['headimgurl']:
                    tasks.download_icon.delay(invite_id, user_info['headimgurl'])
            request.session['username'] = fetch_access_token['openid']
            # 登录跳转
            if 'login_back' in request.session:
                return redirect(request.session['login_back'])
            else:
                return redirect('index')
        else:
            content = {"is_active": Authenticate(request).is_active}
            if re.search("MicroMessenger", request.META['HTTP_USER_AGENT']):
                wx_config = WxConfig.objects.get(id=1)
                if 'iid' in request.GET:
                    wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                         redirect_uri='http://%s/login/' % request.get_host(),
                                         scope='snsapi_userinfo', state=request.GET['iid']).create_url()
                    content.update({"iid": request.GET['iid']})
                else:
                    # 获取微信登录 url
                    wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                         redirect_uri='http://%s/login/' % request.get_host(),
                                         scope='snsapi_userinfo', state='0').create_url()
                content.update({"wx_url": wx_url})
                return render(request, "login.html", content)
            else:
                return render(request, "login.html", content)

    @staticmethod
    def post(request):
        # 用户名登录
        if 'username' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            try:
                customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                if check_password(password, customer.password):
                    request.session['username'] = username
                    request.session['password'] = password
                    cart_goods = CartGoods.objects.filter(anonymous=request.COOKIES['sessionid'])
                    if cart_goods:
                        for c in cart_goods:
                            c.customer = customer
                            c.anonymous = ''
                            c.save()
                    customer.last_ip = request.META['REMOTE_ADDR']
                    customer.login_time = datetime.utcnow().replace(tzinfo=utc)
                    customer.save()
                    return JsonResponse({'msg': 'success'})
                return JsonResponse({"msg": "密码错误，请重新输入！"})
            except CartGoods.DoesNotExist:
                return JsonResponse({"msg": "用户名不存在，请重新输入！"})
        # 手机号登录
        elif 'tel' in request.POST:
            tel = request.POST['tel']
            verify = request.POST['verify']
            try:
                customer = Customer.objects.get(tel=tel)
                if Verify.objects.get(tel=tel).code != verify:
                    return JsonResponse({'msg': '验证码错误,请重新输入！'})
                else:
                    cart_goods = CartGoods.objects.filter(anonymous=request.COOKIES['sessionid'])
                    if cart_goods:
                        for c in cart_goods:
                            c.customer = customer
                            c.anonymous = ''
                            c.save()
                    Verify.objects.filter(tel=tel).delete()
                    request.session['username'] = tel
                    request.session['password'] = customer.password
                    return JsonResponse({'msg': 'success'})
            except CartGoods.DoesNotExist:
                return JsonResponse({'msg': '该手机号未被注册，请点击注册！'})


class FindPwd1View(View):
    # 找回密码视图1
    @staticmethod
    def get(request, p1):
        find_form = FindPwdForm()
        return render(request, "find_pwd1.html", {'find_form': find_form, 'status': p1})

    @staticmethod
    def post(request, p1):
        find_form = FindPwdForm(request.POST)
        tel = request.POST['tel']
        try:
            Customer.objects.get(tel=tel)
            if find_form.is_valid():
                request.session['find_tel'] = tel
                return JsonResponse({"msg": "success"})
            return JsonResponse({'status': p1, "msg": "验证码错误，请重试！"})
        except Customer.DoesNotExist:
            return JsonResponse({'status': p1, "msg": "该手机号不存在，请确认后输入！"})


class FindPwd2View(View):
    # 找回密码视图2
    @staticmethod
    def get(request, p1):
        if 'find_tel' in request.session:
            sms_status = Sms().send_sms(request.session['find_tel'], '一慧文创馆', 'SMS_90025019')
            if sms_status:
                return render(request, "find_pwd2.html", {'status': p1})
            else:
                return render(request, "find_pwd2.html", {'status': p1, 'msg': '该手机号获取过于频繁，请稍后重试！'})

    @staticmethod
    def post(request, p1):
        tel = request.session['find_tel']
        verify = request.POST['verify']
        password = request.POST['password']
        if Verify.objects.get(tel=tel).code != verify:
            return JsonResponse({'status': p1, 'msg': '验证码错误,请重新输入！'})
        else:
            c = Customer.objects.get(tel=tel)
            c.password = make_password(password)
            c.save()
            Verify.objects.filter(tel=tel).delete()
            request.session['username'] = tel
            request.session['password'] = password
            return JsonResponse({'status': p1, 'msg': 'success'})


class MineView(View):
    # 个人中心视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            c = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            return render(request, "mine.html",
                          {'customer': c})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class AccountView(View):
    # 账户管理视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            c = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            if 'logout' in request.GET:
                del request.session['username']
                if 'password' in request.session:
                    del request.session['password']
                return JsonResponse({'msg': 'success'})
            if 'action' in request.GET:
                action = request.GET['action']
                if action == 'name':
                    data = request.GET['data']
                    c.username = data
                    c.save()
                    return JsonResponse({'name': data})
                elif action == 'sex':
                    data = request.GET['data']
                    c.sex = int(data)
                    c.save()
                    print c.get_sex_display()
                    return JsonResponse({'sex': c.get_sex_display()})
                elif action == 'age':
                    birthday = date(int(request.GET['year']), int(request.GET['mouth']), int(request.GET['day']))
                    today = date.today()
                    c.birthday = birthday
                    c.save()
                    age = today.year - birthday.year - 1
                    if today.month > birthday.month:
                        age += 1
                    elif today.month == birthday.month and today.day >= birthday.day:
                        age += 1
                    return JsonResponse({'age': age})
            else:
                age = '--'
                birthday = c.birthday
                if birthday:
                    today = date.today()
                    age = today.year - birthday.year - 1
                    if today.month > birthday.month:
                        age += 1
                    elif today.month == birthday.month and today.day >= birthday.day:
                        age += 1
                return render(request, 'account.html', {'customer': c, 'age': age})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class DeliveryView(View):
    # 收货地址视图
    @staticmethod
    def get(request, q1):
        if Authenticate(request).is_active:
            username = request.session['username']
            if 'action' in request.GET:
                if request.GET['action'] == 'change_default':
                    try:
                        a = Address.objects.get(
                            Q(default=True) & (Q(customers__tel=username) | Q(customers__email=username) | Q(
                                customers__wxoauth__openid=username)))
                        a.default = False
                        a.save()
                        a = Address.objects.get(id=request.GET['id'])
                        a.default = True
                        a.save()
                    except Address.DoesNotExist:
                        a = Address.objects.get(id=request.GET['id'])
                        a.default = True
                        a.save()
                    return JsonResponse({'msg': 'success'})
                elif request.GET['action'] == 'delete':
                    try:
                        Address.objects.get(id=request.GET['id']).delete()
                        return JsonResponse({'msg': 'success'})
                    except Address.DoesNotExist:
                        return JsonResponse({'msg': '删除地址失败'})
            elif 'change_id' in request.GET:
                request.session['address_id'] = request.GET['change_id']
                return JsonResponse({'msg': 'success'})
            else:
                c = Address.objects.filter(
                    Q(customers__tel=username) | Q(customers__email=username) | Q(customers__wxoauth__openid=username))
                return render(request, "delivery.html", {'address': c, 'change': q1})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class DeliveryChangeView(View):
    # 修改收货地址视图
    @staticmethod
    def get(request, q1, q2):
        if Authenticate(request).is_active:
            if 'p' in request.GET:
                return JsonResponse(
                    {'cities': serializers.serialize('json', City.objects.filter(provinces__id=request.GET['p']))})
            elif 'c' in request.GET:
                return JsonResponse(
                    {'areas': serializers.serialize('json', Area.objects.filter(cities__id=request.GET['c']))})
            elif 'delete' in request.GET:
                try:
                    Address.objects.get(id=q2).delete()
                    return JsonResponse({'msg': 'success'})
                except Address.DoesNotExist:
                    return JsonResponse({'msg': 'error'})
            else:
                p = Province.objects.all()
                if q1 == 'edit':
                    c = Address.objects.get(id=q2)
                    return render(request, "delivery_change.html", {'address': c, 'provinces': p, 'method': q1})
                elif q1 == 'add':
                    return render(request, "delivery_change.html", {'provinces': p, 'method': q1})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')

    @staticmethod
    def post(request, q1, q2):
        if q1 == 'edit':
            try:
                username = request.session['username']
                c = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                a = Address.objects.get(id=q2)
                if a.customers == c:
                    a.provinces_id = request.POST['provinces']
                    a.cities_id = request.POST['cities']
                    a.areas_id = request.POST['areas']
                    a.detail = request.POST['detail']
                    a.tel = request.POST['tel']
                    a.recipient = request.POST['recipient']
                    if 'default' in request.POST:
                        addr = Address.objects.get(Q(customers=c) & Q(default=True))
                        addr.default = False
                        addr.save()
                        a.default = True
                    else:
                        a.default = False
                    a.save()
                    return JsonResponse({'msg': 'success'})
                else:
                    return JsonResponse({'msg': '修改添加收货地址失败'})
            except Address.DoesNotExist:
                return JsonResponse({'msg': '修改添加收货地址失败'})
        elif q1 == 'add':
            try:
                username = request.session['username']
                c = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                if 'default' in request.POST:
                    addr = Address.objects.get(Q(customers=c) & Q(default=True))
                    addr.default = False
                    addr.save()
                    default = True
                else:
                    default = not (Address.objects.filter(Q(customers=c) & Q(default=True)))
                Address(customers=c, provinces_id=request.POST['provinces'], cities_id=request.POST['cities'],
                        areas_id=request.POST['areas'], detail=request.POST['detail'], tel=request.POST['tel'],
                        recipient=request.POST['recipient'], default=default).save()
                return JsonResponse({'msg': 'success'})
            except Address.DoesNotExist:
                return JsonResponse({'msg': '添加收货地址失败'})


class OrderView(View):
    # 用户订单视图
    @staticmethod
    def get(request, index):
        if Authenticate(request).is_active:
            username = request.session['username']
            order = Order.objects.order_by('-id').filter(Q(customers__tel=username) | Q(customers__email=username) |
                                                         Q(customers__wxoauth__openid=username))
            return render(request, 'order.html', {'order': order, 'index': index})
        else:
            return redirect('index')


class OrderDetailView(View):
    # 订单详情视图
    @staticmethod
    def confirm(username, order):
        if order.customers.tel == username or order.customers.email == username or \
                order.customers.wxoauth.openid == username:
            return True
        return False

    def get(self, request, oid):
        if Authenticate(request).is_active:
            username = request.session['username']
            if 'delete_id' in request.GET:
                order = Order.objects.get(oid=request.GET['delete_id'])
                if self.confirm(username, order):
                    OrderGoods.objects.filter(order=order).delete()
                    order.delete()
                    return JsonResponse({'msg': 'success'})
                return JsonResponse({'msg': 'failed'})
            elif 'cancel_id' in request.GET:
                order = Order.objects.get(oid=request.GET['cancel_id'])
                if self.confirm(username, order):
                    customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                    customer.coupon.add(order.coupon)
                    OrderGoods.objects.filter(order=order).delete()
                    order.delete()
                    return JsonResponse({'msg': 'success'})
                return JsonResponse({'msg': 'failed'})
            elif 'remind_id' in request.GET:
                order = Order.objects.get(oid=request.GET['remind_id'])
                if self.confirm(username, order):
                    try:
                        remind = RemindOrders.objects.get(order=order)
                        remind.remind_time = datetime.utcnow().replace(tzinfo=utc)
                        remind.save()
                    except RemindOrders.DoesNotExist:
                        RemindOrders(order=order).save()
                    return JsonResponse({'msg': 'success'})
                return JsonResponse({'msg': 'failed'})
            elif 'confirm_id' in request.GET:
                order = Order.objects.get(oid=request.GET['confirm_id'])
                if order.status == 3 and self.confirm(username, order):
                    customer = order.customers
                    oid = order.oid
                    endorsement = Endorsement.objects.filter(id__gte=3).order_by('-id')
                    now = datetime.utcnow().replace(tzinfo=utc)
                    goods_name = " ".join([i.image.goods.name for i in order.ordergoods_set.all()])
                    conf = WechatConf(
                        token='yihui8888',
                        appid='wx5e1f3f920edaf478',
                        appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                        encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                        encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
                    )
                    wechat_instance = WechatBasic(conf=conf)
                    for e in endorsement:
                        if customer.promote + customer.consumption >= Decimal(e.total_amount):
                            customer.classify = e
                            customer.save()
                            break
                    commission = UnableCommission.objects.filter(order=order).order_by('id')
                    for index in range(len(commission)):
                        c = commission[index]
                        spokesman = c.spokesman
                        spokesman.commission += c.commission
                        spokesman.enable_commission += c.commission
                        spokesman.promote += c.order.paid
                        if index == 0:
                            spokesman.promote += order.paid
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
                                                                  "keyword1": {"value": customer.username,
                                                                               "color": "#173177"},
                                                                  "keyword2": {
                                                                      "value": str(now.strftime('%Y年%m月%d日 %H:%M:%S')),
                                                                      "color": "#173177"},
                                                                  "keyword3": {"value": "推荐客户消费提成",
                                                                               "color": "#173177"},
                                                                  "keyword4": {"value": "佣金分成", "color": "#173177"},
                                                                  "keyword5": {"value": str(c.commission),
                                                                               "color": "#173177"},
                                                                  "remark": {"value": "如有疑问，请联系客服！",
                                                                             "color": "#C81522"}
                                                              }, 'endorsement/')

                    order.status = 4
                    order.complete_time = now
                    order.save()
                    wechat_instance.send_template_message(customer.wxoauth.openid,
                                                          'KkX496aShz9F2OW9dj9KqHDaJ4rp_qsNwE8rUzN4K5Y', {
                                                              "first": {"value": "订单已完成，欢迎您下次光临！",
                                                                        "color": "#173177"},
                                                              "keyword1": {"value": oid, "color": "#173177"},
                                                              "keyword2": {"value": goods_name, "color": "#173177"},
                                                              "keyword3": {
                                                                  "value": str(now.strftime('%Y年%m月%d日 %H:%M:%S')),
                                                                  "color": "#173177"},
                                                              "remark": {"value": "感谢您对一慧丝绣的支持！点击查看订单详情",
                                                                         "color": "#C81522"}
                                                          },
                                                          '%sorder_detail/%s' % (domain_name, oid))
                    return JsonResponse({'msg': 'success'})
                else:
                    return JsonResponse({'msg': 'failed'})
            else:
                try:
                    order = Order.objects.get(oid=oid)
                    if self.confirm(username, order):
                        return render(request, 'order_detail.html', {'order': order})
                    return redirect('index')
                except Order.DoesNotExist:
                    return redirect('index')
        else:
            return redirect('index')


class ExpressView(View):
    # 物流查询视图
    @staticmethod
    def get(request, oid):
        if Authenticate(request).is_active:
            username = request.session['username']
            try:
                order = Order.objects.get(oid=oid)
                if order.customers.tel == username or order.customers.email == username or \
                        order.customers.wxoauth.openid == username:
                    exp = express.ExpressSearch(order.express_com.code, order.express_num).get_data()
                    return render(request, 'express.html', {'order': order, 'express': exp})
            except Order.DoesNotExist:
                return redirect('index')
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class CouponView(View):
    # 优惠券列表视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            if 'cid' in request.GET:
                try:
                    c = Coupon.objects.get(id=request.GET['cid'])
                    customer.coupon.add(c)
                    return JsonResponse({'result': 'success'})
                except Coupon.DoesNotExist:
                    return JsonResponse({'result': 'failed'})
            action = request.GET.get('action', '')
            coupon = Coupon.objects.filter(customer=customer)
            is_receive = False
            if action == 'receive':
                coupon = Coupon.objects.filter(Q(is_auto=False) & Q(easy_get=True)).exclude(customer=customer)
                is_receive = True
            return render(request, 'coupon.html', {'coupon': coupon, 'is_receive': is_receive})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class CouponGoodsView(View):
    # 优惠券商品视图
    @staticmethod
    def get(request, cid):
        if Authenticate(request).is_active:
            goods = GoodsList.objects.filter(Q(coupon__id=cid) & Q(to_front=True)).order_by('-sort')
            return render(request, 'promote_list.html', {'goods': goods})
        else:
            return redirect('index')


class CartView(View):
    # 购物车视图
    @staticmethod
    def get(request):
        if 'number' in request.GET:
            cart_goods = CartGoods.objects.get(id=request.GET['id'])
            cart_goods.number = request.GET['number']
            cart_goods.save()
            return JsonResponse({'success': True})
        elif 'del' in request.GET:
            CartGoods.objects.get(id=request.GET['id']).delete()
            return JsonResponse({'success': True})
        elif 'prop' in request.GET:
            cart_goods = CartGoods.objects.get(id=request.GET['id'])
            props = cart_goods.image.goods.get_props()
            return JsonResponse({'success': True, 'props': props})
        elif 'img_id' in request.GET:
            img_id = request.GET['img_id']
            get_cart_goods = CartGoods.objects.get(id=request.GET['cart_goods_id'])
            if Authenticate(request).is_active:
                username = request.session['username']
                try:
                    cart_goods = CartGoods.objects.get(
                        (Q(customer__tel=username) | Q(customer__email=username) |
                         Q(customer__wxoauth__openid=username)) & Q(single=False) & Q(image_id=img_id))
                    cart_goods.number += get_cart_goods.number
                    cart_goods.save()
                    get_cart_goods.delete()
                except CartGoods.DoesNotExist:
                    get_cart_goods.image_id = img_id
                    get_cart_goods.save()
            else:
                try:
                    cart_goods = CartGoods.objects.get(Q(anonymous=request.COOKIES['sessionid']) & Q(image_id=img_id))
                    cart_goods.number += get_cart_goods.number
                    cart_goods.save()
                    get_cart_goods.delete()
                except CartGoods.DoesNotExist:
                    get_cart_goods.image_id = img_id
                    get_cart_goods.save()
            return redirect('cart')
        else:
            hot_goods = GoodsList.objects.filter(Q(is_hot=True) & Q(to_front=True)).order_by('-sort')
            hot_goods = (len(hot_goods) > 8) and hot_goods[:8] or hot_goods
            if Authenticate(request).is_active:
                username = request.session['username']
                cart_goods = CartGoods.objects.filter(
                    (Q(customer__tel=username) | Q(customer__email=username) |
                     Q(customer__wxoauth__openid=username)) & Q(single=False))
                return render(request, 'cart.html', {'goods': cart_goods, 'hot': hot_goods})
            else:
                cart_goods = CartGoods.objects.filter(anonymous=request.COOKIES['sessionid'])
                return render(request, 'cart.html', {'goods': cart_goods, 'hot': hot_goods})

    @staticmethod
    def post(request):
        request.session['cart_id'] = request.POST['cart_id']
        return redirect('cart_commit')


class CartCommitView(View):
    # 提交订单视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            used_coupon = Coupon.objects.filter(id=0)
            coupon = Coupon.objects.filter(customer=customer)
            discount = customer.classify.discount
            red_packet = customer.red_packet
            max_price = Decimal('0.00')
            dis = Decimal('0.00')
            has_freight = False
            if 'address_id' in request.session:
                try:
                    address = Address.objects.get(id=request.session['address_id'])
                except Address.DoesNotExist:
                    address = ""
            else:
                try:
                    address = Address.objects.get(Q(default=True) & (Q(customers=customer)))
                except Address.DoesNotExist:
                    address = ""
            if 'img_id' in request.GET:
                if 'cart_id' in request.session:
                    del request.session['cart_id']
                number = request.GET['number']
                image = Images.objects.get(id=request.GET['img_id'])
                goods = GoodsList.objects.get(images=image)
                try:
                    c = CartGoods.objects.get(Q(customer=customer) & Q(single=True))
                    c.image = image
                    c.number = number
                    c.save()
                except CartGoods.DoesNotExist:
                    CartGoods(customer=customer, number=number, image=image, single=True).save()
                max_price = goods.price * Decimal(number) * discount / 100
                if max_price <= red_packet:
                    red_packet = max_price
                    max_price = 0.00
                else:
                    max_price -= red_packet
                if coupon:
                    for c in coupon:
                        if max_price >= c.full and dis <= c.dis:
                            dis = c.dis
                            used_coupon = c
                    max_price = max_price - dis
                if used_coupon:
                    request.session['coupon_id'] = used_coupon.id
                if max_price < 50:
                    max_price += 10
                    has_freight = True
                return render(request, 'cart_commit.html',
                              {'address': address, 'number': number, 'image': image, 'goods': goods,
                               'red_packet': red_packet, 'discount': discount, 'price': max_price,
                               'coupon': used_coupon,
                               'has_freight': has_freight})
            else:
                cid = request.session['cart_id']
                cid_list = [int(x) for x in cid.split(',')]
                cart_goods = ''
                for i in cid_list:
                    if cart_goods:
                        c = CartGoods.objects.filter(id=i)
                        cart_goods = cart_goods | c
                        max_price += c[0].image.goods.price * Decimal(c[0].number)
                    else:
                        cart_goods = CartGoods.objects.filter(id=i)
                        max_price += cart_goods[0].image.goods.price * Decimal(cart_goods[0].number)
                max_price = max_price * discount / 100
                if max_price <= red_packet:
                    red_packet = max_price
                    max_price = 0.00
                else:
                    max_price -= red_packet
                if coupon:
                    for c in coupon:
                        if max_price >= c.full and dis <= c.dis:
                            dis = c.dis
                            used_coupon = c
                    max_price = max_price - dis
                if used_coupon:
                    request.session['coupon_id'] = used_coupon.id
                if max_price < 50:
                    max_price += 10
                    has_freight = True
                return render(request, 'cart_commit.html', {'address': address, 'cartgoods': cart_goods,
                                                            'coupon': used_coupon, 'customer': customer,
                                                            'red_packet': red_packet, 'discount': discount,
                                                            'price': max_price, 'has_freight': has_freight})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class PayView(View):
    # 付款页面视图
    @staticmethod
    def get(request, oid):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            wx_config = WxConfig.objects.get(id=1)
            if oid:
                order = Order.objects.get(oid=oid)
                content = {'paid': order.paid, 'reduced': order.reduced}
                if 'code' in request.GET:
                    wx_oauth = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret)
                    fetch_access_token = wx_oauth.fetch_access_token(code=request.GET['code'])
                    openid = fetch_access_token['openid']
                    if not WxOauth.objects.filter(openid=openid):
                        WxOauth(customer=customer, openid=openid,
                                access_token=fetch_access_token['access_token'],
                                refresh_token=fetch_access_token['refresh_token']).save()
                        return redirect('pay', oid)
                    else:
                        content['openid'] = True
                elif 'success' in request.GET:
                    if order.status >= 1:
                        return JsonResponse({'msg': 'success'})
                    else:
                        return JsonResponse({'msg': 'fail'})

                if order.customers == customer and order.status == 0:
                    if re.search("MicroMessenger", request.META['HTTP_USER_AGENT']):
                        content['is_wx'] = True
                        content['oid'] = oid
                        try:
                            wx_oauth = WxOauth.objects.get(customer=customer)
                            wx_pay = WeChatPay(appid=wx_config.appid, api_key=wx_config.api_key,
                                               mch_id=wx_config.mch_id)
                            wx_order = wx_pay.order
                            wx_jsapi = wx_pay.jsapi
                            pay_oid = "%d%d" % (int(time.time()) + 1818181818, random.randint(1000, 9999))
                            order.pay_oid = pay_oid
                            order.save()
                            res = wx_order.create("JSAPI", "一慧文创馆--共%s件商品" % order.get_order_goods_nums(),
                                                  str(int(order.paid * 100)),
                                                  'http://%s/pay_success/%s' % (request.get_host(), oid),
                                                  request.META['REMOTE_ADDR'],
                                                  wx_oauth.openid, pay_oid, "%s等%s件商品" % (
                                                      order.ordergoods_set.all()[0].image.goods.name,
                                                      order.get_order_goods_nums()), "公众号支付")
                            jsapi_params = wx_jsapi.get_jsapi_params(res['prepay_id'])
                            content['jsapi'] = jsapi_params
                        except WxOauth.DoesNotExist:
                            wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                                 redirect_uri='http://%s/pay/%s' % (request.get_host(), oid),
                                                 scope='snsapi_userinfo', state='Login').create_url()
                            content['wx_url'] = wx_url
                    return render(request, 'pay.html', content)
                else:
                    return redirect('order', '1')
            else:
                oid = "%d%d" % (int(time.time()), random.randint(1000, 9999))
                discount = customer.classify.discount
                red_packet = customer.red_packet
                if 'address_id' in request.session:
                    address = Address.objects.get(id=request.session['address_id'])
                    del request.session['address_id']
                else:
                    address = Address.objects.get(Q(default=True) & (Q(customers=customer)))
                if 'cart_id' in request.session:
                    cid = request.session['cart_id']
                    cid_list = [int(x) for x in cid.split(',')]
                    paid = Decimal('0.00')
                    for i in cid_list:
                        c = CartGoods.objects.get(id=i)
                        paid += c.image.goods.price * c.number
                    before = paid
                    paid = paid * discount / 100
                    if paid <= red_packet:
                        customer.red_packet = red_packet - paid
                        paid = 0.00
                    else:
                        paid -= red_packet
                        customer.red_packet = 0.00
                    customer.save()
                    if 'coupon_id' in request.session:
                        coupon = Coupon.objects.get(id=request.session['coupon_id'])
                        paid = paid - Decimal(coupon.dis)
                        del request.session['coupon_id']
                        customer.coupon.remove(coupon)
                    if paid < 50:
                        paid += 10
                        freight = 10.00
                    else:
                        freight = 0.00
                    order = Order(oid=oid, customers=customer, address=address, status=0, freight=freight,
                                  reduced=before - paid, paid=paid)
                    order.save()
                    for i in cid_list:
                        c = CartGoods.objects.get(id=i)
                        OrderGoods(order=order, number=c.number, image=c.image).save()
                        c.delete()
                    del request.session['cart_id']
                else:
                    try:
                        c = CartGoods.objects.get(Q(single=True) & Q(customer=customer))
                        paid = c.image.goods.price * c.number
                        before = paid
                        paid = paid * discount / 100
                        if paid <= red_packet:
                            customer.red_packet = red_packet - paid
                            paid = 0.00
                        else:
                            paid -= red_packet
                            customer.red_packet = 0.00
                        customer.save()
                        if 'coupon_id' in request.session:
                            coupon = Coupon.objects.get(id=request.session['coupon_id'])
                            paid = paid - Decimal(coupon.dis)
                            del request.session['coupon_id']
                            customer.coupon.remove(coupon)
                        if paid < 50:
                            paid += 10
                            freight = 10.00
                        else:
                            freight = 0.00
                        order = Order(oid=oid, customers=customer, address=address, status=0, freight=freight,
                                      reduced=before - paid, paid=paid)
                        order.save()
                        OrderGoods(order=order, number=c.number, image=c.image).save()
                        c.delete()
                    except CartGoods.DoesNotExist:
                        return redirect('order', '1')
                    except Coupon.DoesNotExist:
                        return redirect('order', '1')
                return redirect('pay', oid)
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')

    @staticmethod
    def post(request, oid):
        if Authenticate(request).is_active:
            username = request.session['username']
            order = Order.objects.get(oid=oid)
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            if order.customers == customer:
                method = request.POST.get('method', '')
                if method == 'arrive':
                    order.status = 2
                    order.pay_mode = 2
                    order.save()
                return redirect('pay_success', oid)


class AutoPayView(View):
    # 判断跳转微信支付还是支付宝支付
    @staticmethod
    def get(request):
        if re.search("MicroMessenger", request.META['HTTP_USER_AGENT']):
            return redirect('%stransfer' % domain_name)
        elif re.search("AlipayClient", request.META['HTTP_USER_AGENT']):
            return redirect('https://qr.alipay.com/aex00824x9vigpildfdgdfc')
        else:
            return redirect('index')


@csrf_exempt
def pay_success_view(request, oid):
    # 付款成功视图
    if Authenticate(request).is_active:
        username = request.session['username']
        order = Order.objects.get(oid=oid)
        customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
        if request.method == "GET":
            if order.customers == customer:
                return render(request, 'pay_success.html', {'order': order})
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')
    res = WeChatPay().parse_payment_result(request.body)
    xml = u"""
            <xml>
            <return_code><![CDATA[{0}]]></return_code>
            <return_msg><![CDATA[{1}]]></return_msg>
            </xml>
            """
    if res['return_code'] == "SUCCESS":
        order = Order.objects.get(oid=oid)
        if order.status == 0:
            order.status = 1
            order.pay_mode = 1
            order.pay_time = datetime.utcnow().replace(tzinfo=utc)
            order.save()
            address = order.address
            customer = order.customers
            customer.consumption += order.paid
            customer.save()
            oid = order.oid
            pay_time = order.pay_time.strftime('%Y年%m月%d日 %H:%M:%S')
            goods_name = " ".join([i.image.goods.name for i in order.ordergoods_set.all()])
            conf = WechatConf(
                token='yihui8888',
                appid='wx5e1f3f920edaf478',
                appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
            )
            wechat_instance = WechatBasic(conf=conf)
            wechat_instance.send_template_message(customer.wxoauth.openid,
                                                  '1igkBALCJsvJPa4MQ_OeNGBrxxgTO8O2_xf_harVct4',
                                                  {
                                                      "first": {"value": "恭喜你付款成功，店小二正在为您准备红包～", "color": "#173177"},
                                                      "orderProductPrice": {"value": '￥%.2f' % order.paid,
                                                                            "color": "#173177"},
                                                      "orderProductName": {"value": goods_name, "color": "#173177"},
                                                      "orderAddress": {
                                                          "value": " ".join([address.recipient, address.tel,
                                                                             address.provinces.name,
                                                                             address.cities.name, address.areas.name,
                                                                             address.detail]),
                                                          "color": "#173177"},
                                                      "orderName": {"value": oid, "color": "#173177"},
                                                      "remark": {"value": "点击领取现金红包", "color": "#C81522"}
                                                  }, '%sred_packet/%s' % (domain_name, oid))
            if order.customers.invited_id:
                invited = customer.invited
                spokesman1 = Customer.objects.get(invitation=invited)
                commission = "%.2f" % (order.paid * spokesman1.classify.first_commission / 100)
                UnableCommission(spokesman=spokesman1, order=order, commission=commission).save()
                wechat_instance.send_template_message(spokesman1.wxoauth.openid,
                                                      'eW13gUyvr6w8jKezE54M6uhVhe1OncZsz1I4gdgY3PU',
                                                      {
                                                          "first": {
                                                              "value": "您推荐的买家%s付款成功了哦！" %
                                                                       order.customers.username,
                                                              "color": "#173177"},
                                                          "keyword1": {"value": goods_name, "color": "#173177"},
                                                          "keyword2": {"value": str(commission), "color": "#173177"},
                                                          "keyword3": {"value": "已支付", "color": "#173177"},
                                                          "keyword4": {"value": oid, "color": "#173177"},
                                                          "keyword5": {"value": pay_time, "color": "#173177"},
                                                          "remark": {"value": "恭喜你成功推荐！", "color": "#C81522"}
                                                      }, '%sendorsement/' % domain_name)
                if spokesman1.invited_id:
                    invited = spokesman1.invited
                    spokesman2 = Customer.objects.get(invitation=invited)
                    commission = "%.2f" % (order.paid * spokesman2.classify.second_commission / 100)
                    UnableCommission(spokesman=spokesman2, order=order, commission=commission).save()
                    wechat_instance.send_template_message(spokesman2.wxoauth.openid,
                                                          'eW13gUyvr6w8jKezE54M6uhVhe1OncZsz1I4gdgY3PU',
                                                          {
                                                              "first": {
                                                                  "value": "您推荐的买家%s付款成功了哦！" %
                                                                           order.customers.username,
                                                                  "color": "#173177"},
                                                              "keyword1": {"value": goods_name, "color": "#173177"},
                                                              "keyword2": {"value": str(commission),
                                                                           "color": "#173177"},
                                                              "keyword3": {"value": "已支付", "color": "#173177"},
                                                              "keyword4": {"value": oid, "color": "#173177"},
                                                              "keyword5": {"value": pay_time, "color": "#173177"},
                                                              "remark": {"value": "恭喜你成功推荐！", "color": "#C81522"}
                                                          }, '%sendorsement/' % domain_name)
                    if spokesman2.invited_id:
                        invited = spokesman2.invited
                        spokesman3 = Customer.objects.get(invitation=invited)
                        commission = "%.2f" % (order.paid * spokesman3.classify.third_commission / 100)
                        UnableCommission(spokesman=spokesman3, order=order, commission=commission).save()
                        wechat_instance.send_template_message(spokesman3.wxoauth.openid,
                                                              'eW13gUyvr6w8jKezE54M6uhVhe1OncZsz1I4gdgY3PU',
                                                              {
                                                                  "first": {
                                                                      "value": "您推荐的买家%s付款成功了哦！" %
                                                                               order.customers.username,
                                                                      "color": "#173177"},
                                                                  "keyword1": {"value": goods_name, "color": "#173177"},
                                                                  "keyword2": {"value": str(commission),
                                                                               "color": "#173177"},
                                                                  "keyword3": {"value": "已支付", "color": "#173177"},
                                                                  "keyword4": {"value": oid, "color": "#173177"},
                                                                  "keyword5": {"value": pay_time, "color": "#173177"},
                                                                  "remark": {"value": "恭喜你成功推荐！", "color": "#C81522"}
                                                              }, '%sendorsement/' % domain_name)
        xml.format("SUCCESS", "OK")
    else:
        xml.format("FAIL", "NO")
    return HttpResponse(xml, content_type="application/xml")


class TransferView(View):
    # 转账视图
    @staticmethod
    def get(request):
        if re.search("MicroMessenger", request.META['HTTP_USER_AGENT']):
            content = {'is_wx': True}
            wx_config = WxConfig.objects.get(id=1)
            if Authenticate(request).is_active:
                username = request.session['username']
                customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                if 'code' in request.GET:
                    wx_oauth = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret)
                    fetch_access_token = wx_oauth.fetch_access_token(code=request.GET['code'])
                    WxOauth(customer=customer, openid=fetch_access_token['openid'],
                            access_token=fetch_access_token['access_token'],
                            refresh_token=fetch_access_token['refresh_token']).save()
                    return redirect('transfer')
                elif 'paid' in request.GET:
                    paid = Decimal(request.GET['paid']).quantize(Decimal('0.00'))
                    wx_oauth = WxOauth.objects.get(customer=customer)
                    wx_pay = WeChatPay(appid=wx_config.appid, api_key=wx_config.api_key, mch_id=wx_config.mch_id)
                    wx_order = wx_pay.order
                    wx_jsapi = wx_pay.jsapi
                    oid = "%d%d" % (int(time.time()) + 1818181818, random.randint(1000, 9999))
                    try:
                        order = TransferOrders.objects.get(Q(customer=customer) & Q(status=0))
                        wx_order.close(order.oid)
                        order.oid = oid
                        order.paid = paid
                        order.remark = request.GET.get('remark', '')
                        order.save()
                    except TransferOrders.DoesNotExist:
                        TransferOrders(oid=oid, customer=customer, paid=paid,
                                       remark=request.GET.get('remark', '')).save()
                    res = wx_order.create("JSAPI", "一慧文化创意有限公司*扫码收款",
                                          str(int(paid * 100)),
                                          'http://%s/transfer_success/%s' % (request.get_host(), oid),
                                          request.META['REMOTE_ADDR'],
                                          wx_oauth.openid, oid,
                                          "扫码收款",
                                          "扫码收款")
                    jsapi_params = wx_jsapi.get_jsapi_params(res['prepay_id'])
                    content['jsapi'] = jsapi_params
                    content['oid'] = oid
                    return JsonResponse(content)
                elif 'oid' in request.GET:
                    order = TransferOrders.objects.get(oid=request.GET['oid'])
                    if order.status >= 1:
                        return JsonResponse({'msg': 'success'})
                    else:
                        return JsonResponse({'msg': 'fail'})
                else:
                    try:
                        WxOauth.objects.get(customer=customer)
                    except WxOauth.DoesNotExist:
                        wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                             redirect_uri='http://%s/transfer/' % request.get_host(),
                                             scope='snsapi_userinfo', state='Login').create_url()
                        return redirect(wx_url)
            else:
                if 'code' in request.GET:
                    wx_oauth = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret)
                    fetch_access_token = wx_oauth.fetch_access_token(code=request.GET['code'])
                    try:
                        wx_oauth_obj = WxOauth.objects.get(openid=fetch_access_token['openid'])
                        wx_oauth_obj.access_token = fetch_access_token['access_token']
                        wx_oauth_obj.expires_in = fetch_access_token['expires_in']
                        wx_oauth_obj.refresh_token = fetch_access_token['refresh_token']
                        wx_oauth_obj.save()
                    except WxOauth.DoesNotExist:
                        user_info = wx_oauth.get_user_info()
                        invite_id = InvitationManage().get_invite_id()
                        user_icon = '/media/customer/icon/newDefault.png'
                        invitation = Invitation(code=invite_id)
                        invitation.save()
                        customer = Customer(username=user_info['nickname'].encode('iso8859-1'),
                                            user_icon=user_icon, invitation=invitation,
                                            last_ip=request.META['REMOTE_ADDR'])
                        customer.save()
                        WxOauth(customer=customer, openid=fetch_access_token['openid'],
                                access_token=fetch_access_token['access_token'],
                                refresh_token=fetch_access_token['refresh_token']).save()
                        if user_info['headimgurl']:
                            tasks.download_icon.delay(invite_id, user_info['headimgurl'])
                    request.session['username'] = fetch_access_token['openid']
                    return redirect('transfer')
                else:
                    wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                         redirect_uri='http://%s/transfer/' % request.get_host(),
                                         scope='snsapi_userinfo', state='Login').create_url()
                    return redirect(wx_url)
        else:
            content = {'is_wx': False}
        return render(request, 'transfer.html', content)


@csrf_exempt
def transfer_success_view(request, oid):
    # 转账成功视图
    if request.method == "GET":
        if Authenticate(request).is_active and re.search("MicroMessenger", request.META['HTTP_USER_AGENT']):
            try:
                paid = TransferOrders.objects.get(Q(oid=oid) & Q(status=1)).paid
                return render(request, 'transfer_success.html', {'paid': paid})
            except TransferOrders.DoesNotExist:
                return redirect('transfer')
    res = WeChatPay().parse_payment_result(request.body)
    xml = u"""
                <xml>
                <return_code><![CDATA[{0}]]></return_code>
                <return_msg><![CDATA[{1}]]></return_msg>
                </xml>
                """
    if res['return_code'] == "SUCCESS":
        order = TransferOrders.objects.get(oid=oid)
        if order.status == 0:
            order.status = 1
            order.transfer_time = datetime.utcnow().replace(tzinfo=utc)
            order.save()
            username = order.customer.username
            conf = WechatConf(
                token='yihui8888',
                appid='wx5e1f3f920edaf478',
                appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
            )
            wechat_instance = WechatBasic(conf=conf)
            clerk = Customer.objects.filter(clerk=True)
            for c in clerk:
                wechat_instance.send_template_message(c.wxoauth.openid,
                                                      'T_sIFgyeuJg9TAV5teT9EGzw3-3sFh11opM-4n3_G8Y',
                                                      {
                                                          "keyword1": {"value": username, "color": "#173177"},
                                                          "keyword2": {"value": "扫码支付",
                                                                       "color": "#173177"},
                                                          "keyword3":
                                                              {"value": "%.2f" % order.paid, "color": "#173177"},
                                                          "keyword4": {"value":
                                                                       order.transfer_time.replace(
                                                                           tzinfo=pytz.utc).astimezone(
                                                                           pytz.timezone('Asia/Shanghai')).strftime(
                                                                          '%Y年%m月%d日 %H:%M:%S'), "color": "#173177"},
                                                          "remark": {"value": "用户扫码支付成功！", "color": "#C81522"}
                                                      })
        xml.format("SUCCESS", "OK")
    else:
        xml.format("FAIL", "NO")
    return HttpResponse(xml, content_type="application/xml")


class EndorsementView(View):
    # 代言人中心视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            if not customer.classify_id == 5:
                endorsement = Endorsement.objects.get(id=customer.classify_id + 1)
            else:
                endorsement = Endorsement.objects.get(id=customer.classify_id)
            invitation = customer.invitation
            total_customer = invitation.get_customer_num()
            for i in Invitation.objects.filter(invitation_code__invited=invitation):
                total_customer += i.get_customer_num()
                for j in Invitation.objects.filter(invitation_code__invited=i):
                    total_customer += j.get_customer_num()
            return render(request, 'endorsement.html', {'customer': customer, 'total_customer': total_customer,
                                                        'endorsement': endorsement})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class EndorsementTypeView(View):
    # 代言人类型视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            endorsement = Endorsement.objects.all()
            return render(request, 'endorsement_type.html', {'customer': customer, 'endorsement': endorsement})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class EndorsementCashView(View):
    # 佣金提现视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            if 'account' in request.GET:
                try:
                    bank = BankBin.objects.get(bin=request.GET['account'])
                    return JsonResponse({'bank': bank.bank, 'type': bank.type, 'status': 'success'})
                except BankBin.DoesNotExist:
                    return JsonResponse({'status': 'failed'})
            else:
                username = request.session['username']
                customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                try:
                    WxOauth.objects.get(customer=customer)
                    is_authorize = True
                except WxOauth.DoesNotExist:
                    is_authorize = False
                return render(request, 'endorsement_cash.html', {'cash': customer.enable_commission,
                                                                 'is_authorize': is_authorize,
                                                                 'customer': customer.username})
        else:
            return redirect('index')

    @staticmethod
    def post(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            account = request.POST['account']
            name = request.POST['name']
            paid = Decimal(request.POST['cash'])
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            bank = BankBin.objects.get(bin=str(account)[0:6])
            conf = WechatConf(
                token='yihui8888',
                appid='wx5e1f3f920edaf478',
                appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
            )
            wechat_instance = WechatBasic(conf=conf)
            wechat_instance.send_template_message(customer.wxoauth.openid,
                                                  'Ue4HwCSUo_DqDTBeKyNiypE6ivGtB03qKi2vWDkZP1M',
                                                  {
                                                      "first": {
                                                          "value": "您好，提现申请已提交成功！",
                                                          "color": "#173177"},
                                                      "keyword1": {"value": str(paid), "color": "#173177"},
                                                      "keyword2": {"value": "%s(%s)" % (bank.bank, account),
                                                                   "color": "#173177"},
                                                      "keyword3": {"value": str(
                                                          (paid * Decimal('0.99')).quantize(Decimal('0.00'))),
                                                          "color": "#173177"},
                                                      "keyword4": {
                                                          "value": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
                                                          "color": "#173177"},
                                                      "keyword5": {"value": "1-3个工作日内", "color": "#173177"},
                                                      "remark": {"value": "如有疑问，请联系客服！", "color": "#C81522"}
                                                  }, '%sendorsement_cash/' % domain_name)
            try:
                WxOauth.objects.get(customer=customer)
                is_authorize = True
            except WxOauth.DoesNotExist:
                is_authorize = False
            customer.enable_commission -= paid
            customer.save()
            WithdrawOrders(oid="%d%d" % (int(time.time()), random.randint(100, 999)),
                           customer=customer, paid=paid, account=account, name=name, bank=bank).save()
            return render(request, 'endorsement_cash.html', {'status': True, 'cash': customer.enable_commission,
                                                             'is_authorize': is_authorize,
                                                             'customer': customer.username})
        else:
            return redirect('index')


class AuthorizeView(View):
    # 账户管理->微信授权视图
    @staticmethod
    def get(request, status):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            if "code" in request.GET:
                wx_config = WxConfig.objects.get(id=1)
                wx_oauth = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret)
                fetch_access_token = wx_oauth.fetch_access_token(code=request.GET['code'])
                try:
                    wx_oauth_obj = WxOauth.objects.get(openid=fetch_access_token['openid'])
                    wx_oauth_obj.access_token = fetch_access_token['access_token']
                    wx_oauth_obj.refresh_token = fetch_access_token['refresh_token']
                    wx_oauth_obj.save()
                except WxOauth.DoesNotExist:
                    user_info = wx_oauth.get_user_info()
                    invite_id = customer.invitation.code
                    customer.username = user_info['nickname'].encode('iso8859-1')
                    customer.save()
                    WxOauth(customer=customer, openid=fetch_access_token['openid'],
                            access_token=fetch_access_token['access_token'],
                            refresh_token=fetch_access_token['refresh_token']).save()
                    if user_info['headimgurl']:
                        tasks.download_icon.delay(invite_id, user_info['headimgurl'])
                request.session['username'] = fetch_access_token['openid']
                if status == 'account':
                    return redirect('account')
                elif status == 'cash':
                    return redirect('endorsement_cash')
                else:
                    return redirect('mine')
            else:
                if re.search("MicroMessenger", request.META['HTTP_USER_AGENT']):
                    wx_config = WxConfig.objects.get(id=1)
                    wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                         redirect_uri='http://%s/authorize/%s' % (request.get_host(), status),
                                         scope='snsapi_userinfo', state='authorize').create_url()
                    return render(request, "authorize.html", {'wx_url': wx_url})
                else:
                    return redirect('mine')  # 不友好


class PosterView(View):
    # 海报视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            invite_id = customer.invitation.code
            im = InvitationManage(invite_id=invite_id)
            path = im.path
            if not os.path.exists(path):
                im.get_invite_img(request, str(customer.user_icon.url)[7:])

            return render(request, 'poster.html', {'img_url': '/%s' % path})
        else:
            return redirect('index')


class InvitationView(View):
    # 代言人中心->邀请码视图
    @staticmethod
    def get(request):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            invite_id = customer.invitation.code
            if 'invitation' in request.GET:
                conf = WechatConf(
                    token='yihui8888',
                    appid='wx5e1f3f920edaf478',
                    appsecret='c16bb65ea49bc2758236d6f48f02b2e5',
                    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                    encoding_aes_key='rxO7ZYSJEKebQC45xN4fmO51kemB0q4WQnT4E1XwXN0'  # 如果传入此值则必须保证同时传入 token, appid
                )
                wechat_instance = WechatBasic(conf=conf)
                scene_str = invite_id
                dic = wechat_instance.create_qrcode({"expire_seconds": 2592000, "action_name": "QR_STR_SCENE",
                                                     "action_info": {"scene": {"scene_str": scene_str}}})
                return redirect(dic['url'])
            elif 'img' in request.GET:
                im = InvitationManage(invite_id=invite_id)
                qr_path = im.qr_path
                if request.GET['img'] == 'erwei':
                    if not os.path.exists(qr_path):
                        im.get_qrcode(request)
                    return JsonResponse({'img_url': '/%s' % qr_path})
                elif request.GET['img'] == 'tuwen':
                    path = im.path
                    if not os.path.exists(path):
                        im.get_invite_img(request, str(customer.user_icon.url)[7:])
                else:
                    path = ''
                return JsonResponse({'img_url': '/%s' % path})
            elif 'invite_id' in request.GET:
                if invite_id == request.GET['invite_id']:
                    result = 'repeat'
                else:
                    try:
                        invited = Invitation.objects.get(code=request.GET['invite_id'])
                        customer.invited = invited
                        if customer.classify_id == 1:
                            customer.classify_id = 2
                        customer.save()
                        result = 'success'
                    except Invitation.DoesNotExist:
                        result = 'fail'
                return JsonResponse({'result': result})
            return render(request, 'invitation.html', {'invitation': invite_id, 'invited': customer.invited_id})
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class QuestionsView(View):
    # 常见问题视图
    @staticmethod
    def get(request):
        return render(request, 'questions.html', {'questions': NormalQuestion.objects.all().order_by('sort')})


class QuestionDetailView(View):
    # 常见问题详情视图
    @staticmethod
    def get(request, qid):
        try:
            return render(request, 'question_detail.html', {'question': NormalQuestion.objects.get(id=qid)})
        except NormalQuestion.DoesNotExist:
            return redirect('index')


class EBookView(View):
    # 产品电子书视图
    @staticmethod
    def get(request):
        return render(request, 'ebook.html',
                      {'goods': GoodsList.objects.all().order_by('classifylist__classify_one__id')})


class RedPacketView(View):
    # 红包视图
    @staticmethod
    def get(request, oid):
        if Authenticate(request).is_active:
            action = request.GET.get('action', '')
            if action == 'receive':
                try:
                    order = Order.objects.get(oid=oid)
                except Order.DoesNotExist:
                    return redirect('index')
                content = {}
                username = request.session['username']
                customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
                if not order.customers == customer:
                    content['status'] = 'failed'
                    content['warning'] = '这不是您的红包哦～'
                elif order.status not in [1, 2, 3, 4]:
                    content['status'] = 'failed'
                    content['warning'] = '订单未付款或已失效～'
                elif order.received_packet:
                    content['status'] = 'failed'
                    content['warning'] = '该红包已被领取了哦～'
                else:
                    paid = order.paid
                    packet = RedPacket.objects.filter(min_paid__lt=int(paid))
                    rate_sum = 0
                    rate_list = []
                    red_packet = 0.1
                    for p in packet:
                        rate_sum += p.rate
                        rate_list.append([p.money, rate_sum])
                    ran = random.randint(1, rate_sum)
                    for l in rate_list:
                        if ran <= l[1]:
                            red_packet = l[0]
                            break
                    order.received_packet = True
                    order.save()
                    customer.red_packet += red_packet
                    customer.save()
                    content['status'] = 'success'
                    content['red_packet'] = red_packet
                return JsonResponse(content)
            return render(request, 'red_packet.html')
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


class PromoteListView(View):
    # 已推广用户列表
    @staticmethod
    def get(request, action):
        if Authenticate(request).is_active:
            username = request.session['username']
            customer = Customer.objects.get(Q(tel=username) | Q(email=username) | Q(wxoauth__openid=username))
            invitation = customer.invitation
            promote_list = Customer.objects.filter(invited=invitation)
            if action == "first":
                return render(request, 'promote_list.html', {'promote_list': promote_list})
            elif action == "all":
                for i in Invitation.objects.filter(invitation_code__invited=invitation):
                    promote_list = promote_list | Customer.objects.filter(invited=i)
                    for j in Invitation.objects.filter(invitation_code__invited=i):
                        promote_list = promote_list | Customer.objects.filter(invited=j)
                promote_list = promote_list.distinct()
                return render(request, 'promote_list.html', {'promote_list': promote_list})
            else:
                return redirect('endorsement')
        else:
            request.session['login_back'] = request.build_absolute_uri()
            return redirect('login')


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
