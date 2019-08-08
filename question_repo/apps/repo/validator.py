"""
@file:validator.py
@author:李霞丹
@date：2019/08/07
"""

from django.core.exceptions import ValidationError

def valid_difficulty(n):
    if n > 5 or n <1:
        raise ValidationError("难度介于1到5之间")