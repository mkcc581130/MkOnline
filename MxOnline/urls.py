# _*_ encoding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
import xadmin
from django.views.static import serve
from wx.views import wx_view
from users.views import LoginView, RegisterView, FindPwd1View, FindPwd2View, AccountView, DeliveryView, \
    DeliveryChangeView, OrderView, OrderDetailView, ExpressView, CouponView, CouponGoodsView, CartView, CartCommitView,\
    PayView, pay_success_view, DetailView, DifferView, SearchView, MineView, MoreView, TransferView, \
    transfer_success_view, EndorsementView, EndorsementTypeView, EndorsementCashView, AuthorizeView, PosterView, \
    InvitationView, AutoPayView, TelView, QuestionsView, QuestionDetailView, RedPacketView, PromoteListView, EBookView
from users.views import IndexView
from MxOnline.settings import MEDIA_ROOT, STATICFILES_DIRS

urlpatterns = [
    url('^wx$', wx_view, name="wx"),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^reg/$', RegisterView.as_view(), name="reg"),
    url('^find_pwd1/(change|find)*$', FindPwd1View.as_view(), name="find_pwd1"),
    url('^find_pwd2/(change|find)*$', FindPwd2View.as_view(), name="find_pwd2"),
    url('^mine/$', MineView.as_view(), name="mine"),
    url('^detail/(\d*)$', DetailView.as_view(), name="detail"),
    url('^differ/$', DifferView.as_view(), name="differ"),
    url('^search/$', SearchView.as_view(), name="search"),
    url('^more/(\S*)$', MoreView.as_view(), name="more"),
    url('^account/$', AccountView.as_view(), name="account"),
    url('^delivery/(change)*$', DeliveryView.as_view(), name="delivery"),
    url('^delivery_change/(edit|add)*/(\d+)$', DeliveryChangeView.as_view(), name="delivery_change"),
    url('^order/(\d*)$', OrderView.as_view(), name="order"),
    url('^order_detail/(\d*)$', OrderDetailView.as_view(), name="order_detail"),
    url('^express/(\d*)$', ExpressView.as_view(), name="express"),
    url('^coupon/$', CouponView.as_view(), name="coupon"),
    url('^coupon_goods/(\d*)$', CouponGoodsView.as_view(), name="coupon_goods"),
    url('^cart/$', CartView.as_view(), name="cart"),
    url('^cart_commit/$', CartCommitView.as_view(), name="cart_commit"),
    url('^pay/(\d*)$', PayView.as_view(), name="pay"),
    url('^autopay/$', AutoPayView.as_view(), name="autopay"),
    url('^pay_success/(\d*)$', pay_success_view, name="pay_success"),
    url('^transfer/$', TransferView.as_view(), name="transfer"),
    url('^transfer_success/(\d*)$', transfer_success_view, name="transfer_success"),
    url('^endorsement/$', EndorsementView.as_view(), name="endorsement"),
    url('^endorsement_type/$', EndorsementTypeView.as_view(), name="endorsement_type"),
    url('^endorsement_cash/$', EndorsementCashView.as_view(), name="endorsement_cash"),
    url('^tel/$', TelView.as_view(), name="tel"),
    url('^questions/$', QuestionsView.as_view(), name="questions"),
    url('^question_detail/(\d*)$', QuestionDetailView.as_view(), name="question_detail"),
    url('^authorize/(account|cash)*$', AuthorizeView.as_view(), name="authorize"),
    url('^poster/$', PosterView.as_view(), name="poster"),
    url('^red_packet/(\d*)$', RedPacketView.as_view(), name="red_packet"),
    url('^invitation/$', InvitationView.as_view(), name="invitation"),
    url('^ebook/$', EBookView.as_view(), name="ebook"),
    url('^promote_list/(first|all)*$', PromoteListView.as_view(), name="promote_list"),
    url(r'^captcha/', include('captcha.urls')),
    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    #富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^xadmin/', xadmin.site.urls),
]

#全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'