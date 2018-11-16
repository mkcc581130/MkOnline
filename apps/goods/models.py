# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from DjangoUeditor.models import UEditorField
from django.db import models

from users.models import UserProfile
from MxOnline.settings import MEDIA_URL


class ClassifyOne(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"名称")
    en_name = models.CharField(max_length=40, verbose_name=u"Name")
    img = models.ImageField(upload_to="goods/classify/", verbose_name=u"一级分类图片", max_length=100, null=True, blank=True)

    def get_ct_num(self):
        # 获取二级分类数
        return self.classifytwo_set.all().count()
    get_ct_num.short_description = "二级分类数"

    def img_tag(self):
        return u'<img width="50" src="%s%s" />' % (MEDIA_URL, self.img)

    img_tag.short_description = u"图片"
    img_tag.allow_tags = True

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"分类列表"
        verbose_name_plural = verbose_name


class ClassifyTwo(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"名称")
    en_name = models.CharField(max_length=40, verbose_name=u"Name")
    img = models.ImageField(upload_to="goods/classify/", verbose_name=u"二级分类图片", max_length=100, null=True, blank=True)
    sort = models.IntegerField(default=0, verbose_name=u"排序")
    classify_one = models.ForeignKey(ClassifyOne, verbose_name=u"一级分类")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"二级分类"
        verbose_name_plural = verbose_name


class Props(models.Model):
    name = models.CharField(default="", max_length=20, verbose_name=u"名称")
    en_name = models.CharField(default="", max_length=40, verbose_name=u"Name")

    def __unicode__(self):
        return self.name

    def get_dp_num(self):
        return self.detailprops_set.all().count()
    get_dp_num.short_description = "二级属性数"

    class Meta:
        verbose_name = u"属性列表"
        verbose_name_plural = verbose_name


class DetailProps(models.Model):
    name = models.CharField (default="", max_length=20, verbose_name=u"名称")
    en_name = models.CharField(default="", max_length=40, verbose_name=u"Name")
    props = models.ForeignKey(Props, verbose_name="上级属性")

    # def get_gd_num(self):
    #     return self.goodslist_set.all().count()
    # get_gd_num.short_description = "商品数"

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"二级属性"
        verbose_name_plural = verbose_name


class Brand(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"品牌")

    def get_goods(self):
        return self.goodslist_set.all().count()
    get_goods.short_description = "品牌商品数"

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"品牌列表"
        verbose_name_plural = verbose_name


class GoodsList(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"商品名称")
    en_name = models.CharField(max_length=100, verbose_name=u"Goods Name")
    brands = models.ForeignKey(Brand, default=1, verbose_name=u"品牌")
    gid = models.CharField(max_length=20, verbose_name=u"商品编号")
    material_quality = models.CharField(max_length=20, verbose_name=u"材质", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"商品价格")
    have_commission = models.BooleanField(default=True, verbose_name=u"是否有佣金")
    # dis_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"折扣价格")
    # integral = models.IntegerField(verbose_name=u"商品积分")
    to_front = models.BooleanField(default=True, verbose_name=u"上下架")
    sort = models.IntegerField(verbose_name=u"商品排序")
    intr = models.TextField(verbose_name=u"商品简介", null=True, blank=True)
    en_intr = models.TextField (verbose_name=u"Goods Intr", null=True, blank=True)
    detail = UEditorField(verbose_name=u"商品详情", width=900, height=300, imagePath="goods/ueditor/",
                          filePath="goods/ueditor/", null=True, blank=True)
    endetail = UEditorField(verbose_name=u"商品详情（英文）", width=900, height=300, imagePath="goods/ueditor/",
                             filePath="goods/ueditor/", null=True, blank=True)
    visits = models.IntegerField(default=0, verbose_name=u"浏览量")
    counts = models.IntegerField(default=0, verbose_name=u"销售量")
    is_new = models.BooleanField(default=False, verbose_name=u"新品上市")
    is_hot = models.BooleanField(default=False, verbose_name=u"热卖商品")
    is_ex = models.BooleanField(default=False, verbose_name=u"精选商品")
    is_dis = models.BooleanField(default=False, verbose_name=u"限时折扣")
    to_front_time = models.DateTimeField(auto_now_add=True, verbose_name=u"上架时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name=u"修改时间")

    def get_imgs(self):
        img_id = []
        image = self.images_set.all()
        for i in image:
            if i.get_stocks() <= 0:
                img_id.append (i.id)
        if img_id:
            image = image.exclude (id__in=img_id)
        return image

    def img_tag(self):
        img = ''
        for i in self.images_set.all ():
            img += u'<img width="50" style="margin: 0 5px 5px 0" src="%s%s" />' % (MEDIA_URL, i.src)
        return img

    img_tag.short_description = u"图片"
    img_tag.allow_tags = True

    def get_props(self):
        props = []
        for d, i in enumerate(self.get_imgs()):
            prop = i.get_props()
            if d == 0:
                for p in prop:
                    props.append({'prop': p['props'], 'detail_props': [p['detail_props']],
                                  'images': [{'id': str(i.id), 'src': str(i.src)}]})
            else:
                for p in prop:
                    props[prop.index(p)]['detail_props'].append(p['detail_props'])
                    props[prop.index(p)]['images'].append({'id': str(i.id), 'src': str(i.src)})
        return props

    def get_prop(self):
        return self.get_imgs()[0].proplist_set.all()
    # def get_co(self):
    #     return self.classify_two.classify_one

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"商品列表"
        verbose_name_plural = verbose_name


class Visit(models.Model):
    goods = models.ForeignKey(GoodsList, verbose_name=u"商品")
    Visit_time = models.DateTimeField(auto_now_add=True, verbose_name=u"浏览时间")

    def __unicode__(self):
        return self.Visit_time

    class Meta:
        verbose_name = u"浏览量"
        verbose_name_plural = verbose_name


class ClassifyList(models.Model):
    goods = models.ForeignKey(GoodsList, verbose_name=u"商品")
    classify_one = models.ForeignKey(ClassifyOne, verbose_name=u"一级分类")
    classify_two = models.ForeignKey(ClassifyTwo, verbose_name=u"二级分类")

    def __unicode__(self):
        return self.goods.name

    class Meta:
        verbose_name = u"分类"
        verbose_name_plural = u"分类列表"


class Images(models.Model):
    src = models.ImageField(upload_to="goods/image/", verbose_name=u"图片", max_length=100, null=True, blank=True)
    stocks = models.IntegerField(default=0, verbose_name=u"仓库库存量")
    stocks_ht = models.IntegerField(default=0, verbose_name=u"活态馆库存量")
    goods = models.ForeignKey(GoodsList, verbose_name=u"商品", null=True, blank=True)

    def __unicode__(self):
        prop = ""
        for i in self.proplist_set.all():
            prop = prop+"   ---"+i.props.name+"--"+i.detail_props.name
        return self.goods.name+prop

    def get_stocks(self):
        return self.stocks + self.stocks_ht

    def img_tag(self):
        return u'<img width="50" src="%s%s" />' % (MEDIA_URL, self.src)

    img_tag.short_description = u"图片"
    img_tag.allow_tags = True

    def backstage_props(self):
        return self.__unicode__()
    backstage_props.short_description = "总属性"

    def get_props(self):
        prop = []
        for i in self.proplist_set.all():
            prop.append({'props': i.props.name, 'detail_props': i.detail_props.name})
        return prop

    def get_props_all(self):
        prop = ''
        for i in self.proplist_set.all():
            prop += i.props.name+' : ' + i.detail_props.name+' '
        return prop

    class Meta:
        verbose_name = u"库存"
        verbose_name_plural = u"库存列表"


class PropList(models.Model):
    images = models.ForeignKey(Images, verbose_name=u"图片")
    props = models.ForeignKey(Props, verbose_name=u"一级属性")
    detail_props = models.ForeignKey(DetailProps, verbose_name=u"二级属性")

    def __unicode__(self):
        return self.props.name+' '+self.detail_props.name

    class Meta:
        verbose_name = u"图片属性"
        verbose_name_plural = u"图片属性列表"


class ExtraImages(models.Model):
    images = models.ImageField(upload_to="goods/image/extra/",
                               verbose_name=u"图片", max_length=100, null=True, blank=True)
    goods = models.ForeignKey(GoodsList, verbose_name=u"商品")

    def __unicode__(self):
        return self.goods.name

    class Meta:
        verbose_name = u"额外图片"
        verbose_name_plural = u"额外图片列表"


class Coupon(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"优惠券名称")
    goods = models.ManyToManyField(GoodsList, verbose_name=u"商品", blank=True)
    img = models.ImageField (upload_to="goods/coupon/", verbose_name=u"图片", max_length=100, null=True, blank=True)
    full = models.IntegerField(verbose_name=u"满")
    dis = models.IntegerField(verbose_name=u"减")
    explain = models.TextField(verbose_name=u"优惠说明", blank=True)
    is_auto = models.BooleanField(verbose_name=u"是否自动领取", default=True)
    easy_get = models.BooleanField(verbose_name=u"是否能领取", default=True)
    start_time = models.DateTimeField(verbose_name=u"开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name=u"结束时间", null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"优惠券"
        verbose_name_plural = u"优惠券列表"


class Express(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"公司名称")
    code = models.CharField(max_length=10, verbose_name=u"编码")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"快递公司"
        verbose_name_plural = u"快递公司列表"