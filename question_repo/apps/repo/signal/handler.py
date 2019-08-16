"""
@file:handler.py
@author:李霞丹
@date：2019/08/12
"""

from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import QuestionsCollection, UserLog, AnswersCollection

# 收藏题目日志
@receiver(post_save, sender=QuestionsCollection)
def question_collection_log(sender, instance, created, **kwargs):
    if instance.status:
        operate=1
    else:
        operate=2
    UserLog.objects.create(user=instance.user,operate=3,question=instance.question)

# 收藏答案日志（1：收藏，2：取消收藏）
@receiver(post_save, sender=AnswersCollection)
def answer_collection_log(sender, instance, created, **kwargs):
    if instance.status:
        operate = 1
    else:
        operate = 2
    UserLog.objects.create(user=instance.user, operate=operate, answer=instance.answer)


# 当请求完成后，打印一个日志
"""
@receiver(request_finished)
def all_log(sender, **kwargs):
    print(sender, kwargs)
    print("使用信号记日志")
"""


# 当创建一条记录MailLog后，会自动发送邮件
"""
@receiver(post_save, sender=MailLog)
def send_mail(sender, instance, **kwargs):
    pass
"""


"""
import time
@receiver(post_save, sender=UserLog)
def send_mail(sender, instance, **kwargs):
    print(sender, instance, kwargs)
    time.sleep(10)
    print('xxxxxxx发送了一个邮件xxx')
"""