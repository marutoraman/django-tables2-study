from .asin_group import AsinGroupModel
from django.db import models

from django.http import request
from django.utils import timezone
import uuid

class ReplaceWordModel(models.Model):
    
    account_id = models.CharField(max_length=100,default="",verbose_name='アカウントID')
    base_word = models.CharField('対象ワード',max_length=128,null=False)
    replace_word = models.CharField('置換ワード',max_length=128,null=True)
    is_alert = models.BooleanField('アラート表示', default=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)
    
    class Meta():
        db_table='t_replace_word'
        