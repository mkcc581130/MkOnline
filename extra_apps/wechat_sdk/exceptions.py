# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import six

from wechat_sdk.utils import to_binary, to_text


class WechatException(Exception):
    """wechat-python-sdk 异常基类"""
    pass


class WechatAPIException(WechatException):
    """官方 API 错误异常（必须包含错误码及错误信息）"""
    def __init__(self, errcode, errmsg):
        """
        :param errcode: 错误代码
        :param errmsg: 错误信息
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        if six.PY2:
            return to_binary('{code}: {msg}'.format(code=self.errcode, msg=self.errmsg))
        else:
            return to_text('{code}: {msg}'.format(code=self.errcode, msg=self.errmsg))


class WechatSDKException(WechatException):
    """SDK 错误异常（仅包含错误内容描述）"""
    def __init__(self, message=''):
        """
        :param message: 错误内容描述，可选
        """
        self.message = message

    def __str__(self):
        if six.PY2:
            return to_binary(self.message)
        else:
            return to_text(self.message)


class NeedParamError(WechatSDKException):
    """构造参数提供不全异常"""
    pass


class ParseError(WechatSDKException):
    """解析微信服务器数据异常"""
    pass


class NeedParseError(WechatSDKException):
    """尚未解析微信服务器请求数据异常"""
    pass


class OfficialAPIError(WechatAPIException):
    """微信官方API请求出错异常"""
    def __init__(self, errcode, errmsg=None):
        if errmsg is None:  # 对旧版本 OfficialAPIError 的兼容代码
            super(OfficialAPIError, self).__init__(99999, errmsg=errcode)
            return
        super(OfficialAPIError, self).__init__(errcode, errmsg)


class UnOfficialAPIError(WechatSDKException):
    """微信非官方API请求出错异常"""
    pass


class NeedLoginError(UnOfficialAPIError):
    """微信非官方API请求出错异常 - 需要登录"""
    pass


class LoginError(UnOfficialAPIError):
    """微信非官方API请求出错异常 - 登录出错"""
    pass


class LoginVerifyCodeError(LoginError):
    """微信非官方API请求出错异常 - 登录出错 - 验证码错误"""
    pass


class WeChatException(Exception):
    """Base exception for wechatpy"""

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        _repr = 'Error code: {code}, message: {msg}'.format(
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def __repr__(self):
        _repr = '{klass}({code}, {msg})'.format(
            klass=self.__class__.__name__,
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


class WeChatClientException(WeChatException):
    """WeChat API client exception class"""
    def __init__(self, errcode, errmsg, client=None,
                 request=None, response=None):
        super(WeChatClientException, self).__init__(errcode, errmsg)
        self.client = client
        self.request = request
        self.response = response


class InvalidSignatureException(WeChatException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class WeChatPayException(WeChatClientException):
    """WeChat Pay API exception class"""
    def __init__(self, return_code, result_code=None, return_msg=None,
                 errcode=None, errmsg=None, client=None,
                 request=None, response=None):
        """
        :param return_code: 返回状态码
        :param result_code: 业务结果
        :param return_msg: 返回信息
        :param errcode: 错误代码
        :param errmsg: 错误代码描述
        """
        super(WeChatPayException, self).__init__(
            errcode,
            errmsg,
            client,
            request,
            response
        )
        self.return_code = return_code
        self.result_code = result_code
        self.return_msg = return_msg

    def __str__(self):
        if six.PY2:
            return to_binary('Error code: {code}, message: {msg}. Pay Error code: {pay_code}, message: {pay_msg}'.format(
                code=self.return_code,
                msg=self.return_msg,
                pay_code=self.errcode,
                pay_msg=self.errmsg
            ))
        else:
            return to_text('Error code: {code}, message: {msg}. Pay Error code: {pay_code}, message: {pay_msg}'.format(
                code=self.return_code,
                msg=self.return_msg,
                pay_code=self.errcode,
                pay_msg=self.errmsg
            ))

    def __repr__(self):
        _repr = '{klass}({code}, {msg}). Pay({pay_code}, {pay_msg})'.format(
            klass=self.__class__.__name__,
            code=self.return_code,
            msg=self.return_msg,
            pay_code=self.errcode,
            pay_msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

