"""
@file:signals.py.py
@author:李霞丹
@date：2019/08/12
"""

import django.dispatch

# 自定义信号(有两个参数：arg1, arg2)
mysignal = django.dispatch.Signal(providing_args=["arg1","arg2"])

# 内置的信号是自动触发的
# 自定义信号是不能自动触发的