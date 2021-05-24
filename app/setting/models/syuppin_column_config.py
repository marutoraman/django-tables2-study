from django.db import models
from django.http import request
from django.utils import timezone
from config.const import *
from datetime import datetime


class SyuppinColumnConfigModel(models.Model):
    '''
    出品データカラム設定
    '''
    syuppin_column_id = models.CharField("出品カラムID", max_length=64,null=False)
    excel_column_id = models.CharField("ExcelカラムID", max_length=64,null=False)
    
    class Meta:
        db_table='t_syuppin_column_config'
        verbose_name="出品データカラム設定"
    