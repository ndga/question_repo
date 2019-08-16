from django.shortcuts import render, HttpResponse, redirect
import logging
logger = logging.getLogger("account")
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import View,ListView
from django.contrib import auth
from apps.repo.models import Answers,Questions
from django.http import JsonResponse

# Create your views here.

def test(request):
    return HttpResponse("个人中心视图")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "uc_profile.html")

    def post(self, request):
        ret_info = {"code": 200, "msg": "修改成功"}
        try:
            if request.POST.get("email"):
                request.user.email = request.POST.get("email")
            if request.POST.get("mobile"):
                print('change mobile')
                request.user.mobile = request.POST.get("mobile")
            if request.POST.get("qq"):
                request.user.qq = request.POST.get("qq")
            if request.POST.get("realname"):
                request.user.realname = request.POST.get("realname")
            request.user.save()
        except Exception as ex:
            ret_info = {"code": 200, "msg": "修改失败"}
        return render(request, "uc_profile.html", {"ret_info": ret_info})


class ChangePasswdView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'uc_change_passwd.html')

    def post(self, request):
        # from表单提交的数据
        old_password = request.POST.get("oldpassword")
        new_password1 = request.POST.get("newpassword1")
        new_password2 = request.POST.get("newpassword2")

        # 前端验证 new_password1 == new_password2 才能提交
        if new_password1 != new_password2:
            ret_info = {"code": 400, "msg": "新密码不一致"}
        else:
            user = auth.authenticate(username=request.user.username, password=old_password)
            if user:
                user.set_password(new_password1)
                user.save()
                auth.logout(request)
                # auth.update_session_auth_hash(request, user)
                ret_info = {"code":200, "msg":"修改成功"}
                # return render(request, "login.html")
            else:
                ret_info = {"code":400, "msg":"旧密码不正确"}
                # return render(request, "uc_change_passwd.html", {"ret_info":ret_info})
        return render(request, "uc_change_passwd.html", {"ret_info": ret_info})


class AnswerView(LoginRequiredMixin, ListView):
    """
    没有特殊查询条件：Answers.objects.all()
    model = Answers
    template_name = 'uc_answer.html'

    下面是自定义查询：重写get_queryset方法
    """
    # model = Answers
    # default_name: object_list
    # 在页面上的引用名
    context_object_name = "my_answers"
    template_name = 'uc_answer.html'

    def get_queryset(self):
        return Answers.objects.filter(user=self.request.user)


# class ApprovalView(LoginRequiredMixin, View):
#     @method_decorator(permission_required('repo.can_change_question_status', raise_exception=True))
#     def get(self, request):
#         # print()
#         print(request.user.get_all_permissions())
#         questions = Questions.objects.filter(status=False)
#         return render(request, "uc_approval.html", {"questions":questions})
#
#    def post(self, request):
#          pass


# 函数视图: permission_required
# 类视图: PermissionRequiredMixin
# 限制所有请求
class ApprovalView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # 'app.权限'
    permission_required = ('repo.can_change_question_status',)
    # 如果权限不够,是做跳转还是403, True=>403(默认False)
    raise_exception = True

    def get(self, request):
        print(request.user.get_all_permissions())
        questions = Questions.objects.exclude(status=True)
        return render(request, "uc_approval.html", {"questions":questions})


class ApprovalPassView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # 'app.权限'
    permission_required = ('repo.can_change_question_status',)
    # 如果权限不够,是做跳转还是403, True=>403(默认False)
    raise_exception = True

    def get(self, request, id):
        try:
            Questions.objects.filter(id=id).update(status=True)
            ret = {"code":200, "msg":"成功"}
        except:
            ret = {"code":500, "msg":"失败"}
        return JsonResponse(ret)