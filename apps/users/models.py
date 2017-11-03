from datetime import datetime


from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户表
    """
    name = models.CharField(max_length=30, null=True,
                            blank=True, verbose_name='姓名')
    nickname = models.CharField(
        max_length=30, null=True, blank=True, verbose_name='昵称')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    gender = models.CharField(max_length=6, choices=(
        ('male', '男'), ('female', '女')), default='female', verbose_name='性别')
    email = models.EmailField(
        max_length=100, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    email = models.EmailField(
        max_length=100,  verbose_name='邮箱')
    code = models.CharField(max_length=4, verbose_name='验证码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    codeType = models.CharField(max_length=6, choices=(
        ('reg', '注册'), ('reset', '忘记密码')), default='reg', verbose_name='类型')
