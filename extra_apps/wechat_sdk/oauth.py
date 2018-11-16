# -*- coding: utf-8 -*-

from .base import WechatBase
from .lib.request import WechatRequest
from urllib import quote


class WechatOauth(WechatBase):
    def __init__(self, app_id=None, secret=None, redirect_uri=None, scope='snsapi_base', state=''):
        """
                :param app_id: 微信公众号 app_id
                :param secret: 微信公众号 secret
                :param redirect_uri: OAuth2 redirect URI
                :param scope: 可选，微信公众号 OAuth2 scope，默认为 ``snsapi_base``
                    snsapi_base（不弹出授权页面，直接跳转，只能获取用户openid），snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地）。
                :param state: 可选，微信公众号 OAuth2 state，重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节
                """
        self.app_id = app_id
        self.secret = secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state
        self.__request = WechatRequest ()
        self.user_access_token = ''
        self.open_id = ''
        self.refresh_token = ''
        self.user_expires_in = ''

    @property
    def request(self):
        """ 获取当前 WechatConf 配置实例 """
        return self.__request

    def create_url(self):
        url = 'appid'+'='+self.app_id+'&'+'redirect_uri'+'='+quote(self.redirect_uri, safe='')+'&'+'response_type'+'='+'code'+'&'+'scope'+'='+self.scope
        if self.state:
            url += '&'+'state'+'='+self.state
        print url
        return 'https://open.weixin.qq.com/connect/oauth2/authorize?'+url+'#wechat_redirect'

    def fetch_access_token(self, code):
        """获取 access_token

        :param code: 授权完成跳转回来后 URL 中的 code 参数
        :return: JSON 数据包
        """
        res = self.request.get(
            url='https://api.weixin.qq.com/sns/oauth2/access_token',
            params={
                'appid': self.app_id,
                'secret': self.secret,
                'code': code,
                'grant_type': 'authorization_code'
            }
        )
        self.user_access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.user_expires_in = res['expires_in']
        return res

    def refresh_access_token(self, refresh_token):
        """刷新 access token

        :param refresh_token: OAuth2 refresh token
        :return: JSON 数据包
        """
        res = self.request.get (
            url='https://api.weixin.qq.com/sns/oauth2/refresh_token',
            params={
                'appid': self.app_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )

        self.user_access_token = res['access_token']
        self.open_id = res['openid']
        self.refresh_token = res['refresh_token']
        self.user_expires_in = res['expires_in']
        return res

    def get_user_info(self, openid=None, user_access_token=None, lang='zh_CN'):
        """获取用户信息

        :param openid: 可选，微信 openid，默认获取当前授权用户信息
        :param user_access_token: 可选，access_token，默认使用当前授权用户的 access_token
        :param lang: 可选，语言偏好, 默认为 ``zh_CN``
        :return: JSON 数据包
        """
        openid = openid or self.open_id
        user_access_token = user_access_token or self.user_access_token
        return self.request.get (
            url='https://api.weixin.qq.com/sns/userinfo',
            access_token=user_access_token,
            params={
                'openid': openid,
                'lang': lang
            }
        )

    def check_access_token(self, openid=None, user_access_token=None):
        """检查 access_token 有效性

        :param openid: 可选，微信 openid，默认获取当前授权用户信息
        :param user_access_token: 可选，access_token，默认使用当前授权用户的 access_token
        :return: 有效返回 True，否则 False
        """
        openid = openid or self.open_id
        user_access_token = user_access_token or self.user_access_token
        res = self.request.get (
            url='https://api.weixin.qq.com/sns/auth',
            params={
                'access_token': user_access_token,
                'openid': openid
            }
        )
        if res['errcode'] == 0:
            return True
        return False
