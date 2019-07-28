"""
@file:urls.py
@author:李霞丹
@date：2019/07/28
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # 个人资料
    url(r'^profile/$', views.test, name='profile'),
    # 修改密码
    url(r'^change_passwd/$', views.test, name='change_passwd'),
    # 我的回答
    url(r'^answer/$', views.test, name='answer'),
    # 我的收藏
    url(r'^collect/$', views.test, name='collect'),
    # 我的贡献
    url(r'^contribut/$', views.test, name='contribut'),
    # 待审题目
    url(r'^approval/$', views.test, name='approval'),
    # 审核题目
    url(r'^approval/id/$', views.test, name='approval_pass'),
]