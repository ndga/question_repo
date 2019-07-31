"""
@file:urls.py
@author:李霞丹
@date：2019/07/28
"""
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # 注册
    # TemplateView可以不写视图函数
    # url(r'register/$', TemplateView.as_view(template_name="accounts/register.html"), name="register"),
    url(r'register/$', views.Register.as_view(), name="register"),
    # 登录
    url(r'login/$', TemplateView.as_view(template_name="login.html"), name="login"),
    # 退出
    url(r'logout/$', views.test, name="logout"),
    # 忘记密码
    url(r'password/forget/$', views.test, name="password_forget"),
    # 重置密码
    url(r'password/reset/token/$',views.test, name="password_reset"),
]