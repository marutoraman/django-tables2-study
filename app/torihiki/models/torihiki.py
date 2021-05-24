from django.db import models
from django.http import request
from django.utils import timezone
from bulk_update.helper import bulk_update
from django.db.models import F
import json
import uuid
from setting.models.price_setting import *

class TorihikiModel(models.Model):
    
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    yahoo_account_id = models.CharField('ヤフーID',max_length=100,null=False)
    item_name = models.CharField('商品名',max_length=256,default="",null=True)
    asin = models.CharField('ASIN',max_length=12,default="",null=True)
    buied_price = models.IntegerField('落札価格',default=0,null=True)
    amazon_price = models.IntegerField('Amazon価格',default=0,null=True)
    profit = models.IntegerField('利益',default=0,null=True)
    shipping_data = models.CharField('落札価格', max_length=1024, default=0,null=True)
    torihiki_stat = models.IntegerField('取引ステータス',default=0,null=True)
    matome_flg = models.BooleanField('まとめフラグ',default=False,null=True)
    eval_stat = models.IntegerField('評価済フラグ',default=0,null=True)
    shipping_notice_stat = models.IntegerField('発送連絡済フラグ',default=0,null=True)
    auction_id = models.CharField('オークションID',max_length=20,null=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True,null=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True,null=True)
    rakusatsu_at = models.DateTimeField('落札日時',null=True)
    shipped_at = models.DateTimeField('発送完了日時',null=True)
    eval_at = models.DateTimeField('評価実施日時',null=True)
    completed_at = models.DateTimeField('取引完了日時',null=True)
    
    def update_profit(self, account_id, yahoo_account_id):
        # amazon価格が0円より大きい場合は利益を計算する
        obj = TorihikiModel.objects.filter(account_id=account_id, yahoo_account_id=yahoo_account_id, amazon_price__gt = 0)
        obj.update(profit=F('buied_price')-F('amazon_price'))
        #obj.refresh_from_db()
    
    class Meta:
        db_table='t_torihiki_data'
    