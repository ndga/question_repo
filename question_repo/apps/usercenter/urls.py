"""
@file:urls.py
@author:李霞丹
@date：2019/07/28
"""
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView,View

urlpatterns = [
    # 个人资料
    # url(r'^profile/$', TemplateView.as_view(template_name='uc_base.html'), name='profile'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    # 修改密码
    url(r'^change_passwd/$', views.ChangePasswdView.as_view(), name='change_passwd'),
    # 我的回答
    url(r'^answer/$', views.AnswerView.as_view(), name='answer'),
    # 我的收藏
    url(r'^collect/$', views.test, name='collect'),
    # 我的贡献
    url(r'^contribut/$', views.test, name='contribut'),
    # 待审题目
    url(r'^approval/$', views.ApprovalView.as_view(), name='approval'),
    # 审核题目
    url(r'^approval/(?P<id>\d+)/$', views.ApprovalPassView.as_view(), name='approval_pass'),
]


# 同一个url有post方法也有get方法=> 类视图
# 一个url只对应一个方法 => 视图函数/类视图