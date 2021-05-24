from django.db import models
from django.http import request
from django.utils import timezone
from config.const import *
from datetime import datetime


class SyuppinCommonSettingModel(models.Model):
    '''
    出品共通設定
    '''
    account_id=models.CharField("アカウントID", max_length=100,null=False)
    sec_no = models.IntegerField("シーケンスNo",default=0, null=False)
    column_id = models.CharField("項目ID", max_length=64,null=False) 
    column_name = models.CharField("項目名", max_length=64,null=False)
    column_value = models.CharField("設定値", max_length=128,null=True, default=None)
    created_at = models.DateTimeField(default=datetime.now, verbose_name="登録日")
    updated_at = models.DateTimeField(default=datetime.now, verbose_name="更新日")
    
    
    class Meta:
        db_table='t_syuppin_common_setting'
    