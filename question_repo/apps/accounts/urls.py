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
    # url(r'register/$', TemplateView.as_view(template_name="accounts/register.html"), name="register"),
    url(r'^register/$', views.Register.as_view(), name="register"),
    # 登录
    # TemplateView => 基于类的视图 => 不用自己写视图函数
    url(r'^login/$', views.Login.as_view(), name="login"),
    # 退出
    url(r'^logout/$', views.logout, name="logout"),
    # 忘记密码
    url(r'^password/forget/$', views.PasswordForget.as_view(), name="password_forget"),
    # 重置密码
    url(r'^password/reset/(\w+)/$',views.PasswordReset.as_view(), name="password_reset"),
]