from django.db import models

class EvalSettingModel(models.Model):
    
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    yahoo_account_id = models.CharField('ヤフーアカウントID',max_length=100,null=False)
    eval_message = models.CharField('評価メッセージ',max_length=256,null=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)
    
    class Meta():
        db_table='t_eval_message'
        