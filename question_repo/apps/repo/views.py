from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def test(request):
    return HttpResponse("题库视图")

# 要求用户需要登录了才能访问该页面，如果没有登录，跳转到 => '/accounts/login.html'
@login_required
def index(request):
    return render(request, "login.html")