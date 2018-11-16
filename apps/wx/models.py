# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models

from users.models import UserProfile


class WxConfig(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"公众号名称")
    token = models.CharField(max_length=20, verbose_name=u"Token")
    appid = models.CharField(max_length=40, verbose_name=u"应用ID")
    appsecret = models.CharField(max_length=40, verbose_name=u"应用secret")
    encrypt_mode = models.CharField(max_length=15, choices=(("normal", u"明文"), ("compatible", u"兼容"), ("safe", u"安全")))
    encoding_aes_key = models.CharField(max_length=80, verbose_name=u"消息加密密钥")
    access_token = models.CharField(max_length=100, verbose_name=u"ACCESS_TOKEN")
    access_token_expires_at = models.CharField (max_length=20, verbose_name=u"ACCESS_TOKEN有效结束时间")
    mch_id = models.CharField(max_length=40, verbose_name=u"商户ID", null=True)
    api_key = models.CharField(max_length=40, verbose_name=u"商户API密钥", null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"微信配置"
        verbose_name_plural = u"微信配置"


class KeyWord(models.Model):
    keyword = models.CharField (verbose_name=u'关键词', max_length=100, primary_key=True, help_text='用户发出的关键词')
    content = models.TextField (verbose_name=u'内容', null=True, blank=True, help_text='回复给用户的内容')

    pub_date = models.DateTimeField (verbose_name=u'发表时间', auto_now_add=True)
    update_time = models.DateTimeField (verbose_name=u'更新时间', auto_now=True, null=True)
    published = models.BooleanField (verbose_name=u'发布状态', default=True)

    def __unicode__(self):
        return self.keyword

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = '微信回复关键词列表'
