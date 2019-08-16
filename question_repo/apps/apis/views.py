from django.shortcuts import render, HttpResponse, loader
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from libs import sms
import random
import logging
from io import BytesIO
from libs import patcha
import base64
from apps.repo.models import Questions, QuestionsCollection, Answers, AnswersCollection, UserLog
from django.db.models import Q
from django.forms.models import model_to_dict
from django.db import transaction
import os
import time
import datetime
from question_repo.settings import MEDIA_ROOT, MEDIA_URL
logger = logging.getLogger("apis")


# Create your views here.

def get_mobile_captcha(request):
    ret = {"code": 200, "msg": "验证码发送成功！"}
    try:
        mobile = request.GET.get("mobile")
        if mobile is None: raise ValueError("手机号不能为空！")
        mobile_captcha = "".join(random.choices('0123456789', k=6))
        from django.core.cache import cache
        # 将短信验证码写入redis, 300s 过期
        cache.set(mobile, mobile_captcha, 300)
        if not sms.send_sms(mobile, mobile_captcha):
            raise ValueError('发送短信失败')
    except Exception as ex:
        logger.error(ex)
        ret = {"code": 400, "msg": "验证码发送失败！"}
    return JsonResponse(ret)


def get_captcha(request):
    # 直接在内存开辟一点空间存放临时生成的图片
    f = BytesIO()
    # 调用check_code生成照片和验证码
    img, code = patcha.create_validate_code()
    # 将验证码存在服务器的session中，用于校验
    request.session['captcha_code'] = code
    # 生成的图片放置于开辟的内存中
    img.save(f, 'PNG')
    # 将内存的数据读取出来，转化为base64格式
    ret_type = "data:image/jpg;base64,".encode()
    ret = ret_type + base64.encodebytes(f.getvalue())
    del f
    return HttpResponse(ret)


def check_captcah(request):
    ret = {"code": 400, "msg": "验证码错误！"}
    post_captcha_code = request.GET.get('captcha_code', "")
    session_captcha_code = request.session.get("captcha_code")
    print(post_captcha_code, session_captcha_code)
    if post_captcha_code and post_captcha_code.lower() == session_captcha_code.lower():
        ret = {"code": 200, "msg": "验证码正确"}
    return JsonResponse(ret)


class QuestionsView(View):
    def get(self, request):
        """
        :param request:
        :return:
        # /apis/questions/?order=asc&offset=0&limit=25
        """
        # 获取参数
        pagesize = int(request.GET.get("limit", 25))
        offset = int(request.GET.get("offset", 0))
        page = int(request.GET.get("page", 1))
        grade = int(request.GET.get("grade", 0))
        category = int(request.GET.get("category", 0))
        # 2: 不筛选， 1，已刷，0，待刷
        status = int(request.GET.get("status", 1))
        search = request.GET.get("search", "")

        # 取出所有数据，筛选指定等级和分类
        # questions_list = Questions.objects.all()
        questions_list = Questions.objects.filter(status=1)

        if search:
            if search.isdigit():
                questions_list = questions_list.filter(
                    Q(id=search) | Q(content__icontains=search) | Q(title__icontains=search))
            else:
                questions_list = questions_list.filter(Q(content__icontains=search) | Q(title__icontains=search))

        if grade: questions_list = questions_list.filter(grade=grade)
        if category: questions_list = questions_list.filter(category__id=category)

        # 筛选状态 => 我的答题表
        questions_list = questions_list.values('id', 'title', 'grade', 'answer')
        total = len(questions_list)

        # # 计算当前页面的数据
        questions_list = questions_list[offset:offset + pagesize]
        for item in questions_list:
            item["collection"] = True if QuestionsCollection.objects.filter(
                user=request.user, status=True, question_id=item["id"]) else False

        # 格式是bootstrap-table要求的格式
        questions_dict = {'total': total, 'rows': list(questions_list)}
        return JsonResponse(questions_dict, safe=False)


class QuestionCollectionView(LoginRequiredMixin, View):
    def get(self, request, id):
        """
        当用户点击该题目时，首先获取该题目，并检查该题目是否已被操作过
        修改当前题目的收藏状态
        返回json数据
        id => 题目的ID
        """
        try:
            question = Questions.objects.get(id=id)
            with transaction.atomic():
                result = QuestionsCollection.objects.get_or_create(user=request.user, question=question)
                # result是一个元组，第一参数是instance, 第二个参数是true和false
                # True表示新创建,False表示老数据
                question_collection = result[0]
                if not result[1]:
                    # print('x',answer_collection.status)
                    if question_collection.status:
                        question_collection.status = False
                    else:
                        question_collection.status = True
                question_collection.save()
                msg = model_to_dict(question_collection)
                ret_info = {"code": 200, "msg": msg}
        except Exception as ex:
            ret_info = {"code":500, "msg":[]}
        return JsonResponse(ret_info)


class AnswerView(LoginRequiredMixin, View):
    """参考答案"""

    def get(self, request, id):
        # answer = Questions.objects.get(id=id)
        my_answer = Answers.objects.filter(question=id, user=request.user)
        if not my_answer:
            question = {"answer": "请回答后再查看参考答案"}
            return JsonResponse(question, safe=False)

        try:
            # model_to_dict适合Model-Object
            # serializers适合queryset
            # question = model_to_dict(Questions.objects.get(id=id))
            # question = serializers.serialize('json', Questions.objects.filter(id=id))
            # question = serializers.serialize('json', Questions.objects.filter(id=id))
            question = Questions.objects.filter(id=id).values()[0]
        except Exception as ex:
            print(ex)
            question = {}
        return JsonResponse(question, safe=False)


class OtherAnswerView(LoginRequiredMixin, View):
    def get(self, request, id):
        # other_answer = list(Answers.objects.filter(question=id).values())
        # other_answer = serializers.serialize('json', Answers.objects.filter(question=id))
        # return JsonResponse(other_answer, safe=False)

        my_answer = Answers.objects.filter(question=id, user=request.user)
        if not my_answer:
            html = "请回答后再查看其他答案"
            return HttpResponse(html)

        # other_answer = Answers.objects.filter(question=id).exclude(user=request.user)
        other_answer = Answers.objects.filter(question=id)

        if other_answer:
            for answer in other_answer:
                if AnswersCollection.objects.filter(answer=answer, user=request.user, status=True):
                    answer.collect_status = 1  # => 控制爱心=>空心/实心
                # 外键 AnswersCollectionObject.answer=>related_name
                # answer被收藏哪些人收藏了
                # answer.answers_collection_set.filter(status=True)
                answer.collect_nums = answer.answers_collection_set.filter(status=True).count()
                # answer.answers_collection_set
            # 通过后端渲染出HTML
            # html = loader.render_to_string('question_detail_other_answer.html', {"other_answer": other_answer})
            html = loader.get_template('question_detail_other_answer.html').render({"other_answer": other_answer})
        else:
            html = "暂无回答"
        return HttpResponse(html)


class AnswerCollectionView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            answer = Answers.objects.get(id=id)
            with transaction.atomic():
                result = AnswersCollection.objects.get_or_create(user=request.user, answer=answer)
                # result = AnswersCollection.objects.get_or_create(user=request.user, answer_id=1)
                # True表示新创建,False表示老数据
                answer_collection = result[0]
                if not result[1]:
                    # print('x',answer_collection.status)
                    if answer_collection.status:
                        answer_collection.status = False
                    else:
                        answer_collection.status = True
                answer_collection.save()
            msg = model_to_dict(answer_collection)
            logger.info(msg)
            msg["collections"] = answer.answers_collection_set.filter(status=True).count()
            ret_info = {"code": 200, "msg": msg}
            # print(ret_info)
        except Exception as ex:
            ret_info = {"code":500, "msg":[]}
        return JsonResponse(ret_info)
        # return HttpResponse('abc')


class ChangeAvator(LoginRequiredMixin, View):
    def post(self, request):
        today = datetime.date.today().strftime("%Y%m%d")
        # 图片的data-img格式=>data:image/jpg;base64,xxxx
        img_src_str = request.POST.get("image")
        img_str = img_src_str.split(',')[1]
        # 取出格式:jpg/png...
        img_type = img_src_str.split(';')[0].split('/')[1]
        # 取出数据:转化为bytes格式
        img_data = base64.b64decode(img_str)
        # 相对上传路径: 头像上传的相对路径
        avator_path = os.path.join("avator", today)
        # 绝对上传路径：头像上传的绝对路径
        avator_path_full = os.path.join(MEDIA_ROOT, avator_path)
        if not os.path.exists(avator_path_full):
            os.mkdir(avator_path_full)
        filename = str(time.time()) + "." + img_type
        # 绝对文件路径，用于保存图片
        filename_full = os.path.join(avator_path_full, filename)
        # 相对MEDIA_URL路径，用于展示数据
        img_url = f"{MEDIA_URL}{avator_path}/{filename}"
        try:
            with open(filename_full, 'wb') as fp:
                fp.write(img_data)
            ret = {
                "result": "ok",
                "file": img_url
            }
        except Exception as ex:
            ret = {
                "result": "error",
                "file": "upload fail"
            }

        request.user.avator_sor = os.path.join(avator_path, filename)
        request.user.save()
        return JsonResponse(ret)
