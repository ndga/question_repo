from django.db import models
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from .validator import valid_difficulty
from ckeditor.fields import RichTextField
# 含文件上传
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Category(models.Model):
    """分类"""
    name = models.CharField("分类名称", max_length=64)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    """标签"""
    name = models.CharField("标签名", max_length=64)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Questions(models.Model):
    """题库"""
    DIF_CHOICES = (
        (1, "入门"),
        (2, "简单"),
        (3, "中等"),
        (4, "困难"),
        (5, "超难"),
    )
    grade = models.IntegerField("题目难度", choices=DIF_CHOICES, validators=[valid_difficulty], null=True)
    category = models.ForeignKey(Category, verbose_name="所属分类", null=True)
    title = models.CharField("题目标题", unique=True, max_length=256)
    # 富文本编辑器
    content = RichTextUploadingField("题目详情", null=True)
    # 富文本编辑器
    answer = RichTextUploadingField("题目答案", null=True, blank=True)
    contributor = models.ForeignKey(User, verbose_name="贡献者", null=True)
    pub_time = models.DateTimeField("入库时间", auto_now_add=True, null=True)
    # 审核状态
    status = models.BooleanField("审核状态", default=False)
    # 数组....(会产生一个中间表)
    tag = models.ManyToManyField(Tag, verbose_name="题目标签")

    class Meta:
        verbose_name = "题库"
        verbose_name_plural = verbose_name
        permissions = (
                        ('can_change_question', "可以修改题目信息"),
                       ('can_add_question', "可以添加题目信息"),
                       )

    def __str__(self):
        return f"{self.id}:{self.title}"