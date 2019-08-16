from django.db import models
from django.contrib.auth.models import AbstractUser
from easy_thumbnails.fields import ThumbnailerImageField
import os
from question_repo.settings import MEDIA_ROOT, THUMB_SIZE
from libs.images import make_thumb
from django.db.models.fields.files import ImageFieldFile
# Create your models here.

# 继承自AbstractUser
class User(AbstractUser):
    realname = models.CharField(max_length=8, verbose_name="真实姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    qq = models.CharField(max_length=11, verbose_name="QQ号")
    # avator_sor = models.ImageField(upload_to="avator/%Y%m%d/", default="avator/default.jpg", verbose_name="头像")
    avator_sor = ThumbnailerImageField(upload_to="avator/%Y%m%d/", default="avator/default.jpg", verbose_name="头像")
    avator_sm = models.ImageField(verbose_name="头像缩略图", upload_to="avator/%Y%m%d", default='avator/default.70x70.jpg')

    def save(self, *args, **kwargs):
        # 将上传图片先保存
        super().save()
        # 如果是默认图片不压缩
        if self.avator_sor.name == 'avator/default.jpg':
            return
        # 如果文件不存在，不压缩
        if not os.path.exists(os.path.join(MEDIA_ROOT, self.avator_sor.name)):
            return

        base, ext = os.path.splitext(self.avator_sor.name)
        # 从图像中生成缩略图
        thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.avator_sor.name), size=THUMB_SIZE)

        if thumb_pixbuf:
            # 缩略图的保存文件绝对路径 =》 保存文件
            thumb_path = os.path.join(MEDIA_ROOT, base+f'{THUMB_SIZE}x{THUMB_SIZE}'+ext)
            relate_thumb_path = os.path.join('/'.join(self.avator_sor.name.split('/')[:-1]),os.path.basename(thumb_path))
            relate_thumb_path = base + f'.{THUMB_SIZE}x{THUMB_SIZE}' + ext
            thumb_pixbuf.save(thumb_path)
            self.avator_sm = ImageFieldFile(self, self.avator_sm, relate_thumb_path)
            super().save()


class FindPassword(models.Model):
    verify_code = models.CharField(max_length=128, verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱")
    create_time = models.DateTimeField(auto_now=True, verbose_name="重置时间")
    status = models.BooleanField(default=False, verbose_name="是否已重置")