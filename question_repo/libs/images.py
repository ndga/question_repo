"""
@file:images.py
@author:李霞丹
@date：2019/08/14
"""

from PIL import Image

# 生成path图像的缩略图
def make_thumb(path, size):
    pixbuf = Image.open(path)
    width, height = pixbuf.size
    # 如果宽度大于size
    if width > size:
        delta = width / size
        height = int(height / delta)
        pixbuf.thumbnail((size, height), Image.ANTIALIAS)
        return pixbuf