from django.db import models

class ProfitModel(models.Model):
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    base_price = models.IntegerField('価格レンジ',default=0,null=False)
    profit = models.IntegerField('利益額',default=0,null=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)

    class Meta():
        db_table='t_profit'