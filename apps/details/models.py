from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Detail(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    content = models.CharField(max_length=1000, verbose_name="正文")
    user = models.ForeignKey(User, related_name='auther',verbose_name="作者")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    
    class Meta:
        verbose_name = '内容'
        verbose_name_plural = verbose_name
        # unique_together = ("user",'content')