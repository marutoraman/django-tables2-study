from django.db import models

class SearchWordModel(models.Model):
    account_id = models.CharField('アカウントID',max_length=100,null=False)
    search_word = models.TextField('検索キーワード',max_length=64,null=False)
    search_site = models.CharField('検索サイト',max_length=10,null=False)
    max_page_num = models.IntegerField('最大ページ数',default=1)
    is_completed = models.BooleanField('完了フラグ',default=False)
    created_at = models.DateTimeField('作成日時',auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)

    class Meta():
        db_table='t_search_word'