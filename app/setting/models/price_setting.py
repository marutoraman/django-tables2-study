from logging import Logger
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request
from django.utils import timezone

### 出品価格設定
class PriceSettingModel(models.Model):
    account_id=models.CharField(max_length=100,default="",verbose_name='アカウントID')
    yahoo_account_id=models.CharField(max_length=50,default="",verbose_name="ヤフオクアカウントID")
    price_range1=models.IntegerField(default=2000,verbose_name='価格レンジ1')
    price_rate1=models.FloatField(default=1.5,verbose_name='倍率1')
    price_range2=models.IntegerField(default=5000,verbose_name='価格レンジ2')
    price_rate2=models.FloatField(default=1.5,verbose_name='倍率2')
    price_range3=models.IntegerField(default=7000,verbose_name='価格レンジ3')
    price_rate3=models.FloatField(default=1.5,verbose_name='倍率3')
    price_range4=models.IntegerField(default=10000,verbose_name='価格レンジ4')
    price_rate4=models.FloatField(default=1.5,verbose_name='倍率4')
    price_range5=models.IntegerField(default=999999,verbose_name='価格レンジ5')
    price_rate5=models.FloatField(default=1.5,verbose_name='倍率5')
    sokketsu_price_offset=models.IntegerField(default=0,verbose_name='開始価格と即決価格の差額')

    class Meta():
        db_table='t_price_setting'