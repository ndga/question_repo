"""
@file:context_processors.py
@author:李霞丹
@date：2019/08/13
"""
from . import settings

def site_info(request):
    # 站点基本信息
    site = {}
    site["SITE_NAME"] = settings.SITE_NAME
    site["SITE_DESC"] = settings.SITE_DESC
    site["SITE_KEYWORDS"] = settings.SITE_KEYWORDS
    # site["SITE_URL"] = settings.SITE_URL
    # site["PRO_GIT"] = settings.PRO_GIT
    # site["PRO_RSS"] = settings.PRO_RSS
    # site["WEIBO_URL"] = settings.WEIBO_URL
    return locals()