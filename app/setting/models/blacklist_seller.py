from django.db import models

class BlacklistSellerModel(models.Model):
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    seller_name = models.TextField('除外セラー',max_length=64,null=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)

    class Meta():
        db_table='t_blacklist_seller'