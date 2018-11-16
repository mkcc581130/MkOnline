# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from DjangoUeditor.models import UEditorField
from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=50, verbose_name=u"标题")
    index = models.IntegerField(verbose_name=u"排序")
    img = models.ImageField(upload_to="banner/image/com/", verbose_name=u"电脑大图")
    mobile_img = models.ImageField(upload_to="banner/image/mobile/", verbose_name=u"手机小图")
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u"添加时间")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = u"轮播图列表"


class Verify(models.Model):
    tel = models.CharField(max_length=12, verbose_name=u"手机号")
    code = models.CharField(max_length=8, verbose_name=u"验证码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"生成时间")

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = u"验证码"
        verbose_name_plural = u"验证码列表"


class Endorsement(models.Model):
    name = models.CharField(max_length=10, verbose_name=u"代言人规则名")
    first_commission = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name=u"一级推广佣金比")
    second_commission = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name=u"二级推广佣金比")
    third_commission = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name=u"三级推广佣金比")
    discount = models.IntegerField(verbose_name=u"折扣")
    total_amount = models.IntegerField(default=0, verbose_name=u"累计推广加消费金额")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"生成时间")

    def __unicode__(self):
        return self.name

    def get_customer_num(self):
        # 获取客户数
        return self.customer_set.all().count()
    get_customer_num.short_description = "代言人数"

    class Meta:
        verbose_name = u"代言人规则"
        verbose_name_plural = u"代言人规则列表"


class NormalQuestion(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"问题标题")
    content = UEditorField(verbose_name=u"问题内容", width=900, height=300, imagePath="management/question/",
                           filePath="management/question/", null=True, blank=True)
    sort = models.IntegerField (verbose_name=u"排序", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"生成时间")
    modify_time = models.DateTimeField(verbose_name=u"修改时间", null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"常见问题"
        verbose_name_plural = u"常见问题列表"


class RedPacket(models.Model):
    money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"红包金额")
    rate = models.IntegerField (verbose_name=u"频率")
    min_paid = models.IntegerField (default=0, verbose_name=u"最少支付金额")
    enable = models.BooleanField(default=True, verbose_name=u"是否可用")

    def __unicode__(self):
        return "%s元红包 --- %s" % (self.money, self.rate)

    class Meta:
        verbose_name = u"红包"
        verbose_name_plural = u"红包列表"