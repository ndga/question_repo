from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Questions
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def test(request):
    return HttpResponse("题库视图")


# 要求用户需要登录了才能访问该页面，如果没有登录，跳转到 => '/accounts/login.html'
@login_required
def index(request):
    return render(request, "index.html")

@login_required
def questions(request):
    category = Category.objects.all()
    grades = Questions.DIF_CHOICES
    search = request.GET.get("search","")
    kwgs = {"category":category,
            "grades":grades,
            "search_key":search
            }
    return  render(request, "questions.html", kwgs)

class QuestionsList(LoginRequiredMixin,View):
    def get(self, request):
        category = Category.objects.all().values("id", "name")
        grades = Questions.DIF_CHOICES
        # 添加search参数，以便搜索刷新后在页面上还能看到搜索的关键字
        search_key = request.GET.get("search", "")
        kwgs = {"category":category, "grades":grades, "search_key":search_key}
        return render(request, 'questions.html', kwgs)

class QuestionDetail(View):
    def get(self, request, id):
        return render(request, "question_detail.html")