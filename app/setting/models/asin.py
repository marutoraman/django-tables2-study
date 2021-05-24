from .asin_group import AsinGroupModel
from django.db import models

from django.http import request
from django.utils import timezone
import uuid

class AsinModel(models.Model):
    
    account_id = models.CharField(max_length=100,default="",verbose_name='アカウントID')
    asin_group_id = models.ForeignKey(AsinGroupModel, on_delete=models.CASCADE)
    #asin_group_id = models.ForeignKey(AsinGroupModel,to_field='asin_group_id',on_delete=models.CASCADE) # ASINグループIDと紐付ける（削除時はこちらも削除）
    asin = models.CharField('ASIN',max_length=20,null=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)
    
    class Meta():
        db_table='t_asin'
        