from django.db import models
from django.http import request
from django.utils import timezone
from bulk_update.helper import bulk_update
import json
import uuid
import ulid
from datetime import datetime


class SampleModel(models.Model):
    
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField('商品名',max_length=256,null=False)
    item_id = models.CharField('商品ID',max_length=64,null=False,default="")
    description = models.CharField('商品説明',default="",max_length=1024)
    price = models.IntegerField('価格',default=0)
