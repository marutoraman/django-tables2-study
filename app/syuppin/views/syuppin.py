from agent.engine.fetch_mercari_item import * 
from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django_tables2 import SingleTableView, RequestConfig
from ..models.syuppin import *
from setting.models.fetch_url import *
from ..tables.syuppin import * 
from ..forms.item_search import *
from config.const import * 
from django.contrib.auth import get_user_model
import openpyxl
import os
from syuppin.engine.excel import *
from app.settings import BASE_DIR

User = get_user_model()

class SyuppinItemView(SingleTableView):
    table_class = SyuppinItemTable
    template_name = "syuppin/item_list.html"

    # テーブルを生成するための情報を取得
    def get(self, request, *args, **kwargs):

        return self.render_data(request)
        
    def post(self, request, *args, **kwargs):
        # 商品を取得
        if "fetch-item" in request.POST:
            # 編集情報をアップデート
            url_objects = FetchUrlModel.objects.filter(account_id=request.user, is_completed=False)
            urls = [obj.url for obj in url_objects]
            items = FetchMercariItem.fetch_mercari_items(urls)
        elif "export-excel" in request.POST:
            # Excelファイルを作成してダウンロード
            filename = FILENAME.SYUPPIN_EXCEL.format(DATETIME=datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            
            # ページに表示されているItemを出力
            item_ids = request.POST.getlist("pk")
            item_objects = SyuppinItemModel.objects.filter(account_id=request.user, pk__in=item_ids).all()
            # import pprint
            # pprint.pprint([item.__dict__ for item in item_objects])
            wb,work_filename = create_excel(request.user, item_objects)
            
            response = HttpResponse(content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'attachment; filename={filename}'
            wb.save(response)
            
            # 作業用のExcelファイルを削除
            os.remove(work_filename)
            
            # 出力済フラグを付与
            for obj in item_objects:
                obj.is_export_completed = True
                #SyuppinItemModel.objects.filter(account_id=request.user).update(is_export_completed=True)
                obj.save()
            
            return response
        elif "save-item-data" in request.POST:
            item_data_list=request.POST.getlist("post_item_data")
            SyuppinItemModel.update_item_data(item_data_list)
        elif "delete" in request.POST:
            # 選択したレコードを削除
            checkbox_selection = request.POST.getlist("checkbox")
            SyuppinItemModel.objects.filter(id__in=checkbox_selection).delete()
        elif "delete_row" in request.POST:
            # 選択したレコードを削除
            delete_row = request.POST.get("delete_row")
            SyuppinItemModel.objects.filter(account_id=request.user, id=delete_row).delete()
        elif "delete-export-all" in request.POST:
            # 選択したレコードを削除
            SyuppinItemModel.objects.filter(account_id=request.user, is_export_completed=True).delete()
        elif "delete-all" in request.POST:
            SyuppinItemModel.objects.filter(account_id=request.user).delete()
        
        return self.render_data(request)

    
    def render_data(self,request,**kwargs):
        # データ表示処理
        items = SyuppinItemModel.objects.filter(account_id=request.user).order_by("pk").all()
        table = SyuppinItemTable(items)
        # １ページの表示件数の制御
        per_page = request.GET.get("per_page") if request.method == "GET" else request.POST.get("per_page")
        per_page = per_page if per_page != None else 25
        RequestConfig(request, paginate={'per_page': per_page}).configure(table)

        # 取得の進捗状況
        all_count = FetchUrlModel.objects.filter(account_id=request.user).all().count()
        completed_count = FetchUrlModel.objects.filter(account_id=request.user, is_completed=True).all().count()
        context = {'table': table, 
                   'record_count': items.count(),
                   'all_count': all_count,
                   'completed_count': completed_count,
                   'progress': int(completed_count/all_count * 100)
                  }
        
        return render(request, self.template_name, context)
    
    
    def check_syuppin_data(self,syuppin_data):
        for data in syuppin_data:
            if not(data.syuppin_price > 0 or data.description != ""):
               return False 
           
        return True

        
     

        





