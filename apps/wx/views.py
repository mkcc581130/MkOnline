# _*_ encoding:utf-8 _*_
from wechat_sdk import WechatConf, WechatBasic, WechatOauth
from wechat_sdk.messages import TextMessage, EventMessage
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import KeyWord, WxConfig
from customers.models import Customer, WxOauth, City
from goods.models import GoodsList
from MkOnline.settings import MEDIA_URL
import requests
import json
# 初始化
wei_config = WxConfig.objects.get(id=1)
conf = WechatConf(
    token=wei_config.token,
    appid=wei_config.appid,
    appsecret=wei_config.appsecret,
    encrypt_mode=wei_config.encrypt_mode,  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key=wei_config.encoding_aes_key  # 如果传入此值则必须保证同时传入 token, appid
)
wechat_instance = WechatBasic(conf=conf)
# 域名地址
domain_name = "http://101.132.38.60/"


# 接受微信请求函数
@csrf_exempt
def wx_view(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')
        return HttpResponse(request.GET.get('echostr', ''))
    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except IOError:
        return HttpResponseBadRequest('Invalid XML Data')
    # 获取解析好的微信请求信息
    response = None
    message = wechat_instance.get_message()
    # 关注回复
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '修改自定义菜单':
            # 回复修改自定义菜单，快速修改
            wechat_instance.create_menu({
                'button': [
                    {
                        'type': 'view',
                        'name': '绣坊首页',
                        'url': domain_name,
                        'sub_button': []
                    }, {
                        'name': '一慧挚友',
                        'sub_button': [
                            {
                                'type': 'view',
                                'name': '个人中心',
                                'url': '{}mine'.format(domain_name),
                                'sub_button': []
                            }, {
                                'type': 'view',
                                'name': '我要代言',
                                'url': '{}endorsement'.format(domain_name),
                                'sub_button': []
                            }, {
                                'type': 'view',
                                'name': '如何代言',
                                'url': '{}questions'.format(domain_name),
                                'sub_button': []
                            }, {
                                'type': 'view',
                                'name': '代言人二维码',
                                'url': '{}poster'.format(domain_name),
                                'sub_button': []
                            }
                        ]
                    }, {

                        "name": "联系我们",
                        'sub_button': [{
                                'type': 'view',
                                'name': '问卷调查',
                                'url': 'https://www.wjx.cn/jq/22888594.aspx',
                                'sub_button': []
                            }, {
                                "type": "click",
                                'name': '联系地址',
                                "key": "contact",
                                'sub_button': []
                            }]
                    }
                ]})
            response = wechat_instance.response_text(content='修改成功')
        else:
            try:
                # 查询数据库中的回复关键字
                keyword_object = KeyWord.objects.get(keyword=content)
                reply_text = keyword_object.content
                response = wechat_instance.response_text(content=reply_text)
            except KeyWord.DoesNotExist:
                # 默认回复
                try:
                    reply_text = KeyWord.objects.get(keyword='提示').content
                    response = wechat_instance.response_text(content=reply_text)
                except KeyWord.DoesNotExist:
                    response = wechat_instance.group_transfer_message()

    elif isinstance(message, EventMessage):
        # 点击事件
        if message.type == 'click':
            if message.key == 'contact':
                reply_text = '联系电话：0571-89193963 \n联系地址：浙江省杭州市拱墅区小河路450号中国扇博物馆 手工艺活态馆内'
                response = wechat_instance.response_text(content=reply_text)
        # 关注事件
        elif message.type == 'subscribe':
            # 判断关注是否带有推荐码参数
            if message.key:
                wx_config = WxConfig.objects.get(id=1)
                try:
                    key = json.loads(message.key[8:])
                    url = '/detail/{}'.format(key['gid'])
                    iid = key['iid']
                    goods = GoodsList.objects.get(id=key['gid'])
                    title = goods.name
                    picurl = '{}{}{}'.format(domain_name, MEDIA_URL, str(goods.get_imgs()[0].src))
                except GoodsList.DoesNotExist:
                    iid = message.key[8:]
                    url = '/login'
                    title = u'微信登录购买享九五折优惠'
                    picurl = u'{}static/img/yihuigz2.jpg'.format(domain_name)
                wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                     redirect_uri='http://{}{}'.format(request.get_host(), url),
                                     scope='snsapi_userinfo', state=iid).create_url()
                response = wechat_instance.response_news([{
                    'title': u'丝尚杭州 绣绎杭城\n——欢迎来到一慧文创',
                    'description': u'一慧欢迎您',
                    'picurl': u'{}static/img/yihuigz3.png'.format(domain_name),
                    'url': u'http://mp.weixin.qq.com/s/lG3ARqkKBUq-ND2ZKXyQGg',
                }, {
                    'title': u'弘扬传统文化\n——为杭城丝绣代言',
                    'picurl': u'{}static/img/gz-sz1.jpg'.format(domain_name),
                    'url': u'{}endorsement'.format(domain_name),
                }, {
                    'title': title,
                    'picurl': picurl,
                    'url': wx_url,
                }])
            else:
                response = wechat_instance.response_news([{
                    'title': u'丝尚杭州 绣绎杭城\n——欢迎来到一慧文创',
                    'description': u'一慧欢迎您',
                    'picurl': u'{}static/img/yihuigz3.png'.format(domain_name),
                    'url': u'http://mp.weixin.qq.com/s/lG3ARqkKBUq-ND2ZKXyQGg',
                }, {
                    'title': u'弘扬传统文化\n——为杭城丝绣代言',
                    'picurl': u'{}static/img/gz-sz1.jpg'.format(domain_name),
                    'url': u'{}endorsement'.format(domain_name),
                }, {
                    'title': u'一慧绣坊\n——只为最美的你',
                    'picurl': u'{}static/img/gz-wj.jpg'.format(domain_name),
                    'url': domain_name,
                }])
        # 扫描二维码事件
        elif message.type == 'scan':
            wx_config = WxConfig.objects.get(id=1)
            try:
                key = json.loads(message.key)
                url = '/detail/{}'.format(key['gid'])
                iid = key['iid']
                goods = GoodsList.objects.get(id=key['gid'])
                title = goods.name
                picurl = '{}{}{}'.format(domain_name, MEDIA_URL, str(goods.get_imgs()[0].src))
                print picurl
            except GoodsList.DoesNotExist:
                iid = message.key
                url = '/login'
                title = u'微信登录购买享九五折优惠'
                picurl = u'{}static/img/yihuigz2.jpg'.format(domain_name)
            wx_url = WechatOauth(app_id=wx_config.appid, secret=wx_config.appsecret,
                                 redirect_uri='http://{}{}'.format(request.get_host(), url),
                                 scope='snsapi_userinfo', state=iid).create_url()
            response = wechat_instance.response_news([{
                'title': u'丝尚杭州 绣绎杭城\n——欢迎来到一慧文创',
                'description': u'一慧欢迎您',
                'picurl': u'{}static/img/yihuigz3.png'.format(domain_name),
                'url': u'http://mp.weixin.qq.com/s/lG3ARqkKBUq-ND2ZKXyQGg',
            }, {
                'title': u'弘扬传统文化\n——为杭城丝绣代言',
                'picurl': u'{}static/img/gz-sz1.jpg'.format(domain_name),
                'url': u'{}endorsement'.format(domain_name),
            }, {
                'title': title,
                'picurl': picurl,
                'url': wx_url,
            }])
        # 获取地理位置事件
        elif message.type == 'location':
            try:
                wx_oauth = WxOauth.objects.get(openid=message.source)
                wx_oauth.latitude = message.latitude
                wx_oauth.longitude = message.longitude
                wx_oauth.save()
                if wx_oauth.access_token:
                    r = requests.request(
                        method='get',
                        url='http://apis.map.qq.com/ws/geocoder/v1/?location={},{}&coord_type=1&get_poi=1&key=QM4BZ-7QCW6-Y5PSV-MKY2Y-IM5XF-NLFGN'.format(str(message.latitude), str(message.longitude))
                    )
                    r.raise_for_status()
                    address = r.json()
                    c = Customer.objects.get(wxoauth=wx_oauth)
                    c.area = City.objects.get(name=address["result"]["address_component"]["city"])
                    c.save()
            except WxOauth.DoesNotExist:
                response = None
    # 响应相应请求
    return HttpResponse(response, content_type="application/xml")
