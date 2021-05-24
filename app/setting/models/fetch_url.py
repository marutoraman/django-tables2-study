from django.db import models

class FetchUrlModel(models.Model):
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    url = models.TextField('URL',max_length=64,null=False)
    is_completed = models.BooleanField('完了フラグ',default=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)

    class Meta():
        db_table='t_fetch_url'