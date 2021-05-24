from django.db import models
from django.http import request
from django.utils import timezone
from config.const import *

# 出品設定
class SampleModel(models.Model):
    '''
    サンプルForm用のモデル
    '''
    # Form側で選択肢を表示させたい場合は、choicesに対してタプル配列を指定する
    account_id=models.CharField(max_length=100,default="",verbose_name='アカウントID',choices=())
    auction_mode=models.CharField(max_length=10,default="オークション",verbose_name="オークション/フリマ選択",choices=SELECTION.AUCTION_MODE)
    units=models.IntegerField(default=1,verbose_name='個数')
    kaisai_kikan=models.IntegerField(default=1,verbose_name='開催期間',choices=SELECTION.KAISAI_KIKAN)
    end_time=models.IntegerField(default=22,verbose_name='終了時間',choices=SELECTION.END_TIME)
    shipping_address=models.CharField(max_length=10,default="東京都",verbose_name="商品発送元の都道府県",choices=SELECTION.TODOUFUKEN)
    souryou_futan=models.CharField(max_length=10,default="落札者",verbose_name="送料負担",choices=SELECTION.SOURYOU_FUTAN)
    item_condition=models.CharField(max_length=10,default="未使用",verbose_name="商品の状態")
    hyouka_seigen=models.CharField(max_length=10,default="いいえ",verbose_name="入札者評価制限",choices=SELECTION.YES_NO)
    bad_hyouka_seigen=models.CharField(max_length=10,default="いいえ",verbose_name="悪い評価の割合での制限",choices=SELECTION.YES_NO)
    nyuusatsusya_ninsyou_seigen=models.CharField(max_length=10,default="いいえ",verbose_name="入札者認証制限",choices=SELECTION.YES_NO)
    auto_extention=models.CharField(max_length=10,default="はい",verbose_name="自動延長",choices=SELECTION.YES_NO)
    fast_end=models.CharField(max_length=10,default="はい",verbose_name="早期終了",choices=SELECTION.YES_NO)
    auto_saisyuppin=models.IntegerField(default=3,verbose_name="自動再出品",choices=SELECTION.AUTO_SAI_SYUPPIN)
    shipping_date=models.CharField(max_length=10,default="2～3日",verbose_name="発送までの日数",choices=SELECTION.SHIPPING_DATE)
    other_shipping_method=models.CharField(max_length=20,default="委託配送会社",verbose_name="配送方法１")
    other_shipping_price=models.IntegerField(default=1200,verbose_name="配送方法１の一律価格")
    # 長さが不定の場合はTextFieldを使用する場合が多い（多用するとDBのパフォーマンスが低下する場合があるので注意）
    description_template=models.TextField(default="<CENTER>$$description$$</CENTER>",verbose_name="説明文テンプレート(　$$description$$　を商品説明を入れたい箇所に入力してください)")
    syuppin_sleep_sec = models.IntegerField("出品毎の待ち時間(秒)", default=5)
    
    # 任意のテーブル名を指定できる
    # （未指定だと、Djangoがapp名、class名から自動的に命名するが、わかりずらいので自分で指定した方が良い）
    class Meta:
        db_table='sample'
    