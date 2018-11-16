# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from goods.models import GoodsList, Coupon, PropList, Images, Express
from management.models import Endorsement


class Province(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"省")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"省"
        verbose_name_plural = verbose_name


class City(models.Model):
    provinces = models.ForeignKey(Province, verbose_name=u"省")
    name = models.CharField(max_length=30, verbose_name=u"市")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"市"
        verbose_name_plural = verbose_name


class Area(models.Model):
    cities = models.ForeignKey(City, verbose_name=u"市")
    name = models.CharField(max_length=40, verbose_name=u"区")
    zipcode = models.IntegerField(verbose_name=u"邮编")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"区"
        verbose_name_plural = verbose_name


class Invitation(models.Model):
    code = models.CharField(max_length=12, verbose_name=u"邀请码", null=True, blank=True)

    def __unicode__(self):
        return self.code

    def get_customer_num(self):
        return self.invited_code.all().count()

    get_customer_num.short_description = "总用户数"

    def get_order_num(self):
        count = 0
        customer = Customer.objects.filter(invited__code=self.invitation_code)
        for c in customer:
            count += c.get_order_num()
        return count

    get_customer_num.short_description = "总邀请订单数"

    class Meta:
        verbose_name = u"邀请码"
        verbose_name_plural = u"邀请码列表"


class Customer(models.Model):
    username = models.CharField(default="一慧会员", max_length=100, verbose_name=u"用户昵称")
    password = models.CharField(max_length=150, verbose_name=u"密码", null=True, blank=True)
    tel = models.CharField(max_length=12, verbose_name=u"手机号", null=True, blank=True)
    email = models.EmailField(verbose_name=u"邮箱", null=True, blank=True)
    sex = models.IntegerField(verbose_name=u"性别", choices=((1, u"男"), (2, u"女")), null=True, blank=True)
    birthday = models.DateField(verbose_name=u"出生年月", null=True, blank=True)
    area = models.ForeignKey(City, verbose_name=u"所在城市", null=True, blank=True)
    user_icon = models.ImageField(default="/media/customer/icon/newDefault.png", upload_to="customer/icon/",
                                  verbose_name=u"用户头像", max_length=150, null=True, blank=True)
    classify = models.ForeignKey(Endorsement, default=1, verbose_name=u"代言人级别")
    coupon = models.ManyToManyField(Coupon, default="", verbose_name=u"已领取优惠券", blank=True)
    red_packet = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=u"红包")
    invitation = models.OneToOneField(Invitation, verbose_name=u"邀请码", related_name=u"invitation_code", null=True,
                                      blank=True)
    invited = models.ForeignKey(Invitation, verbose_name=u"被邀请码", related_name=u"invited_code", null=True,
                                blank=True)
    consumption = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=u"消费额")
    promote = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=u"推广额")
    commission = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=u"总佣金")
    enable_commission = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=u"余额")
    clerk = models.BooleanField(default=False, verbose_name=u"职员")
    reg_time = models.DateTimeField(auto_now_add=True, verbose_name=u"注册时间")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name=u"最后登录时间")
    last_ip = models.URLField(default="", verbose_name=u"最后登录ip地址", null=True, blank=True)
    follow = models.ManyToManyField(GoodsList, verbose_name=u"关注商品", blank=True)

    def __unicode__(self):
        return self.username

    def get_order_num(self):
        # 获取订单数
        return self.order_set.all().count()

    get_order_num.short_description = "总订单数"

    class Meta:
        verbose_name = u"客户"
        verbose_name_plural = u"客户列表"


class WxOauth(models.Model):
    customer = models.OneToOneField(Customer, verbose_name=u"用户")
    openid = models.CharField(max_length=100, verbose_name=u"OpenID", null=True, blank=True)
    access_token = models.CharField(max_length=200, verbose_name=u"ACCESS_TOKEN", null=True, blank=True)
    refresh_token = models.CharField(max_length=200, verbose_name=u"REFRESH_TOKEN", null=True, blank=True)
    latitude = models.CharField(max_length=30, verbose_name=u"REFRESH_TOKEN", null=True, blank=True)
    longitude = models.CharField(max_length=30, verbose_name=u"REFRESH_TOKEN", null=True, blank=True)

    def __unicode__(self):
        return self.customer.username

    class Meta:
        verbose_name = u"微信登录信息"
        verbose_name_plural = u"微信登录信息列表"


class Address(models.Model):
    customers = models.ForeignKey(Customer, verbose_name=u"客户")
    recipient = models.CharField(default=u"", max_length=12, verbose_name=u"收件人")
    tel = models.CharField(default=u"", max_length=12, verbose_name=u"手机号")
    provinces = models.ForeignKey(Province, verbose_name=u"省")
    cities = models.ForeignKey(City, verbose_name=u"市")
    areas = models.ForeignKey(Area, verbose_name=u"区")
    detail = models.CharField(max_length=100, default=u"", verbose_name=u"详细地址")
    default = models.BooleanField(verbose_name=u"默认地址", default=False)

    def __unicode__(self):
        return self.provinces.name + self.cities.name + self.areas.name + u" " + self.detail + u" " + self.tel

    class Meta:
        verbose_name = u"收货地址"
        verbose_name_plural = u"收货地址列表"


class Order(models.Model):
    oid = models.CharField(default=u"", max_length=16, verbose_name=u"订单编号")
    customers = models.ForeignKey(Customer, verbose_name=u"客户")
    address = models.ForeignKey(Address, verbose_name=u"收货地址", null=True, blank=True)
    status = models.IntegerField(verbose_name=u"订单状态",
                                 choices=((0, u"待付款"), (1, u"已支付"), (2, u"待发货"), (3, u"已发货"), (4, u"已完成"),
                                          (5, u"已关闭"), (6, u"退款中")))
    pay_mode = models.IntegerField(verbose_name=u"支付方式",
                                   choices=((0, u"支付宝支付"), (1, u"微信支付"), (2, u"货到付款")), null=True, blank=True, )
    express_com = models.ForeignKey(Express, verbose_name=u"快递公司", null=True, blank=True)
    express_num = models.CharField(default=u"", max_length=30, verbose_name=u"快递单号", null=True, blank=True)
    info = models.CharField(max_length=100, verbose_name=u"备注", null=True, blank=True)
    freight = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, verbose_name=u"运费")
    reduced = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name=u"已优惠")
    paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"实付金额")
    # integral_get = models.IntegerField(verbose_name=u"获得积分数", null=True, blank=True)
    invitation = models.ForeignKey(Invitation, verbose_name=u"邀请码", null=True, blank=True)
    coupon = models.ForeignKey(Coupon, verbose_name=u"优惠券", null=True, blank=True)
    discount = models.IntegerField(default=100, verbose_name=u"折扣")
    received_packet = models.BooleanField(default=False, verbose_name=u"是否领取红包")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"订单创建时间")
    remind_pay = models.BooleanField(default=False, verbose_name=u"提醒支付")
    pay_time = models.DateTimeField(verbose_name=u"付款时间", null=True, blank=True)
    delivery_time = models.DateTimeField(verbose_name=u"发货时间", null=True, blank=True)
    complete_time = models.DateTimeField(verbose_name=u"订单完成时间", null=True, blank=True)
    pay_oid = models.CharField(max_length=40, verbose_name=u"支付订单号", null=True, blank=True)

    def __unicode__(self):
        return self.oid

    def get_order_goods(self):
        image = []
        order_goods = self.ordergoods_set.all()
        if order_goods.count() == 1:
            i = order_goods[0].image
            return {'num': order_goods[0].number, 'image': i.src, 'id': i.goods.id, 'goods': i.goods.name,
                    'price': i.goods.price, 'prop': i.get_props()}
        else:
            for g in order_goods:
                i = g.image
                image.append({'num': g.number, 'image': i.src, 'id': i.goods.id, 'goods': i.goods.name,
                              'price': i.goods.price, 'prop': i.get_props_all()})
            return image

    def get_order_goods_num(self):
        return self.ordergoods_set.all().count()

    def get_order_goods_nums(self):
        num = 0
        for o in self.ordergoods_set.all():
            num += o.number
        return str(num)

    class Meta:
        verbose_name = u"订单号"
        verbose_name_plural = u"订单列表"


class CartGoods(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=u"用户", null=True, blank=True)
    anonymous = models.CharField(max_length=40, verbose_name=u"匿名号", null=True, blank=True)
    number = models.IntegerField(verbose_name=u"数量")
    image = models.ForeignKey(Images, verbose_name=u"图片", default=1)
    single = models.BooleanField(verbose_name=u"是否直接购买", default=False)

    def __unicode__(self):
        return self.image.goods.name + u"*" + str(self.number)

    class Meta:
        verbose_name = u"购物车商品"
        verbose_name_plural = u"购物车商品列表"


class OrderGoods(models.Model):
    order = models.ForeignKey(Order, verbose_name=u"所属订单")
    number = models.IntegerField(verbose_name=u"数量")
    image = models.ForeignKey(Images, verbose_name=u"图片", default=1)
    evaluate_level = models.IntegerField(verbose_name=u"评价等级",
                                         choices=((0, u"差评"), (1, u"中评"), (2, u"好评")), null=True, blank=True)
    evaluate = models.TextField(verbose_name=u"评价详情", null=True, blank=True)
    evaluate_time = models.DateTimeField(verbose_name=u"评价时间", null=True, blank=True)

    def __unicode__(self):
        return self.image.goods.name + u"*" + str(self.number)

    class Meta:
        verbose_name = u"订单商品"
        verbose_name_plural = u"订单商品列表"


class RemindOrders(models.Model):
    order = models.ForeignKey(Order, verbose_name=u"提醒订单")
    remind_time = models.DateTimeField(auto_now=True, verbose_name=u'提醒时间')

    def __unicode__(self):
        return self.order

    class Meta:
        verbose_name = u"提醒发货"
        verbose_name_plural = u"提醒发货列表"


class TransferOrders(models.Model):
    oid = models.CharField(default=u"", max_length=16, verbose_name=u"订单编号", null=True)
    customer = models.ForeignKey(Customer, verbose_name=u"所属客户")
    paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"实付金额")
    status = models.IntegerField(verbose_name=u"状态", choices=((0, u"未付款"), (1, u"已成功")), default=0)
    remark = models.CharField(max_length=80, verbose_name=u"备注", null=True)
    transfer_time = models.DateTimeField(verbose_name=u'转账时间', auto_now=True, null=True)

    def __unicode__(self):
        return self.customer.username + "--" + str(self.paid)

    class Meta:
        verbose_name = u"转账订单"
        verbose_name_plural = u"转账订单列表"


class ReturnGoods(models.Model):
    order = models.ForeignKey(Order, verbose_name=u"所属订单")
    order_goods = models.ManyToManyField(OrderGoods, verbose_name=u"退货商品")
    refund = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"退款金额")
    reason = models.TextField(verbose_name=u"退货原因")
    status = models.IntegerField(verbose_name=u"退货订单状态", choices=((0, u"审核中"), (1, u"退货中"), (2, u"退款成功")))
    express_num = models.CharField(default=u"", max_length=16, verbose_name=u"退货快递单号", null=True, blank=True)
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name=u"申请时间")
    complete_time = models.DateTimeField(verbose_name=u"完成时间", null=True, blank=True)

    def __unicode__(self):
        return self.order.oid

    class Meta:
        verbose_name = u"退货订单"
        verbose_name_plural = u"退货订单列表"


class BankBin(models.Model):
    bank = models.CharField(max_length=30, verbose_name=u"银行名称", null=True)
    bin = models.CharField(max_length=20, verbose_name=u"bin", null=True)
    type = models.CharField(max_length=30, verbose_name=u"卡类型", null=True)

    def __unicode__(self):
        return self.bank + '--' + self.bin

    class Meta:
        verbose_name = u"银行BIN"
        verbose_name_plural = u"银行BIN列表"


class WithdrawOrders(models.Model):
    oid = models.CharField(max_length=16, verbose_name=u"订单编号", null=True)
    customer = models.ForeignKey(Customer, verbose_name=u"所属客户")
    paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"提现金额")
    name = models.CharField(max_length=16, verbose_name=u"姓名", null=True)
    account = models.CharField(max_length=20, verbose_name=u"银行账号", null=True)
    bank = models.ForeignKey(BankBin, verbose_name=u"所属银行", null=True)
    status = models.IntegerField(verbose_name=u"提现状态", choices=((0, u"未处理"), (1, u"已处理")), default=0)
    withdraw_time = models.DateTimeField(auto_now_add=True, verbose_name=u'提现时间')
    handing_time = models.DateTimeField(verbose_name=u'处理时间', null=True)

    def __unicode__(self):
        return self.customer.username + "--" + str(self.paid)

    class Meta:
        verbose_name = u"提现订单"
        verbose_name_plural = u"提现订单列表"


class UnableCommission(models.Model):
    spokesman = models.ForeignKey(Customer, verbose_name=u"推广人")
    order = models.ForeignKey(Order, verbose_name=u"所属订单")
    commission = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=u"未结算佣金")
    is_settled = models.BooleanField(default=False, verbose_name=u"是否结算")
    settled_time = models.DateTimeField(verbose_name=u"结算时间", null=True, blank=True)

    def __unicode__(self):
        return self.spokesman.username + "=>" + self.order.customers.username + " " + str(self.commission)

    class Meta:
        verbose_name = u"未结算佣金"
        verbose_name_plural = u"未结算佣金列表"
