from django.db import models
from django.http import request
from django.utils import timezone
import uuid

class AsinGroupModel(models.Model):
    
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    yahoo_account_id = models.CharField('ヤフーアカウントID',max_length=100,null=False)
    asin_group_id = models.CharField('ASINグループID',max_length=100,null=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)
    started_at = models.DateTimeField('取得開始日時',null=True)
    asin_count = models.IntegerField('ASIN数',default=0)
    completed_count = models.IntegerField('完了ASIN数',default=0)
    completed_at = models.DateTimeField('完了日時',null=True)
    
    class Meta():
        db_table='t_asin_group'
        