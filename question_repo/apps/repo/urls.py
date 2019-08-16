"""
@file:urls.py
@author:李霞丹
@date：2019/07/28
"""

from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    # 主页
    # url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^index/$', views.index, name="index"),
    # 题目列表
    url(r'^questions/$', views.QuestionsList.as_view(), name="questions"),
    # 贡献题目
    url(r'^question/$', views.Question.as_view(), name="question"),
    # 题目详情，捕获了一个参数
    url(r'^question/(?P<id>\d+)/$', views.QuestionDetail.as_view(), name="question_detail"),
    # 分页
    # url(r'^paginator/(?P<page>\d+)/$', views.PageView.as_view(), name="paginator"),
    url(r'^paginator/$', views.PageView.as_view(), name="paginator"),
]