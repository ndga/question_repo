"""
@file:urls.py
@author:李霞丹
@date：2019/07/28
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # 获取手机验证码
    url(r'^get_mobile_captcha/$', views.get_mobile_captcha, name='get_mobile_captcha'),
    # 获取图片验证码
    url(r'^get_captcha/$', views.get_captcha, name="get_captcha"),
    url(r'^check_captcha/$', views.check_captcah, name="check_captcha")
    ]
