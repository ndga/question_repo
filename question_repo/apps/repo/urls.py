"""
@file:urls.py
@author:李霞丹
@date：2019/07/28
"""

from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.test, name='index'),
    # 题目列表
    url(r'^questions/$', views.test, name="questions"),
    # 贡献题目
    url(r'^question/$', views.test, name="question"),
    # 题目详情，捕获了一个参数
    url(r'^question/id/$', views.test, name="question_detail"),
]