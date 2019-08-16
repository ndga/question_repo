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
    url(r'^check_captcha/$', views.check_captcah, name="check_captcha"),
    # 获取题目
    url(r'^questions/$', views.QuestionsView.as_view(), name='questions'),
    # 收藏题目功能爱心
    url(r'^question/collection/(?P<id>\d+)/$', views.QuestionCollectionView.as_view(), name='question_collection'),
    # 参考答案接口
    url(r'^answer/(?P<id>\d+)/$', views.AnswerView.as_view(), name="answer"),
    # 某题所有人的回答接口
    url(r'^other_answer/(?P<id>\d+)/$', views.OtherAnswerView.as_view(), name="other_answer"),
    # 收藏其他答案
    url(r'^answer/collection/(?P<id>\d+)/$', views.AnswerCollectionView.as_view(), name='answer_collection'),
    # 上传个人中心的头像图片
    url(r'^change_avator/$', views.ChangeAvator.as_view(), name='change_avator'),
]
