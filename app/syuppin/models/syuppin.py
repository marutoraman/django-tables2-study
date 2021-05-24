from django.db import models
from django.http import request
from django.utils import timezone
from bulk_update.helper import bulk_update
import json
import uuid
import ulid
from datetime import datetime


class SyuppinItemModel(models.Model):
    
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    item_name = models.CharField('商品名',max_length=256,null=False)
    item_id = models.CharField('商品ID',max_length=64,null=False,default="")
    item_sku = models.CharField('商品SKU',max_length=32,null=False,default=uuid.uuid4)
    description = models.CharField('商品説明',default="",max_length=1024)
    price = models.IntegerField('価格',default=0)
    amazon_price = models.IntegerField('販売価格',default=0)
    category = models.CharField('カテゴリ',max_length=50, default="")
    brand = models.CharField('ブランド',max_length=50, default="")
    thumbnail_url = models.CharField('サムネイル',max_length=256, default="")
    image_url1 = models.TextField('画像1',default="",null=True)
    image_url2 = models.TextField('画像2',default="",null=True)
    image_url3 = models.TextField('画像3',default="",null=True)
    image_url4 = models.TextField('画像4',default="",null=True)
    image_url5 = models.TextField('画像5',default="",null=True)
    image_url6 = models.TextField('画像6',default="",null=True)
    image_url7 = models.TextField('画像7',default="",null=True)
    image_url8 = models.TextField('画像8',default="",null=True)
    image_url9 = models.TextField('画像9',default="",null=True)
    image_url10 = models.TextField('画像10',default="",null=True)
    is_image1_selected = models.CharField('画像1選択', max_length=10, default="checked")
    is_image2_selected = models.CharField('画像2選択', max_length=10, default="")
    is_image3_selected = models.CharField('画像3選択', max_length=10, default="")
    is_image4_selected = models.CharField('画像4選択', max_length=10, default="")
    is_image5_selected = models.CharField('画像5選択', max_length=10, default="")
    is_image6_selected = models.CharField('画像6選択', max_length=10, default="")
    is_image7_selected = models.CharField('画像7選択', max_length=10, default="")
    is_image8_selected = models.CharField('画像8選択', max_length=10, default="")
    is_image9_selected = models.CharField('画像9選択', max_length=10, default="")
    is_image10_selected = models.CharField('画像10選択',max_length=10, default="")
    condition = models.CharField('商品の状態',max_length=20, default="")
    shipping_payment = models.CharField('配送料負担',max_length=20, default="")
    shipping_method = models.CharField('配送料方法',max_length=20, default="")
    shipping_prefecture = models.CharField('配送元',max_length=20, default="")
    shipping_leadtime = models.CharField('配送までの期間',max_length=20, default="")
    seller_name = models.CharField('販売者名',max_length=50, default="")
    is_export_completed = models.BooleanField('出力完了フラグ', default=False)
    is_alert = models.BooleanField('アラート表示フラグ', default=False)
    site = models.CharField('取得元サイト', max_length=20)
    url = models.TextField("URL",default="")
    created_at = models.DateTimeField('作成日時',default=datetime.now)
    updated_at = models.DateTimeField('更新日時',default=datetime.now)
    
    class Meta:
        db_table='t_syuppin_item'
        
    @staticmethod
    def update_item_data(item_data_list):
        update_object=[]
        # １ページ分の更新データを全て処理する
        for item_data in item_data_list:
            item_data=json.loads(item_data)
            # 更新用オブジェクトを作成
            update_object.append(
                SyuppinItemModel(
                    pk=item_data["id"],
                    amazon_price = item_data["amazon_price"] if item_data["amazon_price"].isnumeric() else 0,
                    item_name=item_data["item_name"],
                    description=item_data["description"],
                    is_image1_selected = item_data["is_image1_selected"],
                    is_image2_selected = item_data["is_image2_selected"],
                    is_image3_selected = item_data["is_image3_selected"],
                    is_image4_selected = item_data["is_image4_selected"],
                    is_image5_selected = item_data["is_image5_selected"]
                    )
                )
        # 更新
        bulk_update(update_object, update_fields=['amazon_price','item_name','description','is_image1_selected',
                                                  'is_image2_selected','is_image3_selected','is_image4_selected',
                                                  'is_image5_selected'])
        
        
    def is_selected_image(self, image_index:int) -> bool:
        '''
        画像nの選択有無を判別
        '''
        if self.__dict__.get(f"is_image{image_index}_selected"):
            return True if self.__dict__[f"is_image{image_index}_selected"] == "checked" else False
        else:
            return False