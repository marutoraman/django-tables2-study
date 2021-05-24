from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.contrib import messages
from django_tables2 import SingleTableView, RequestConfig
from users.models import User,YahooAccount
from ..tables.status import *

class StatusView(SingleTableView):
    table_class = StatusViewTable
    template_name = "syuppin/status.html"

    def get(self, request, *args, **kwargs):
        item_obj = AsinGroupModel.objects.filter(account_id=self.request.user) # 出品登録されていないものを表示
        table_data = StatusViewTable(item_obj)  # テーブルに格納
        RequestConfig(request).configure(table_data)  # ソートに必要
        return render(request, self.template_name, {'table': table_data})

    def post(self, request, *args, **kwargs):
        # 削除
        if "delete" in request.POST:
            # 選択したレコードを削除
            checkbox_selection = request.POST.getlist("checkbox")
            print(checkbox_selection)
            # ASINsetrtinテーブルおよびAsingetidテーブルから削除
            asin_group_obj=AsinGroupModel.objects.filter(id__in=checkbox_selection)
            for obj in asin_group_obj:
                AsinGroupModel.objects.filter(account_id=self.request.user,
                                              asin_group_id=obj.asin_group_id).delete()
                       
            # データ取得
            item_obj = AsinGroupModel.objects.filter(account_id=self.request.user) # 出品登録されていないものを表示
            table_data = StatusViewTable(item_obj)  # テーブルに格納
            RequestConfig(request).configure(table_data)  # ソートに必要
            
            return render(request, self.template_name, {'table': table_data})