"""
@file:views.py.py
@author:李霞丹
@date：2019/07/26
"""
from django.shortcuts import HttpResponse
import logging

# apis为settings中Logging配置中的loggers
logger = logging.getLogger('apis')

def logtest(request):
    logger.info("欢迎访问")
    return HttpResponse('日志测试')