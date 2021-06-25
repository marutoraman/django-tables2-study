from django.shortcuts import render
from django_tables2 import SingleTableView, RequestConfig
from ..models.sample import *
from ..tables.sample import * 
from ..forms.item_search import *

class SampleView(SingleTableView):
    table_class = SampleTable
    template_name = "sample/item_list.html"

    # テーブルを生成するための情報を取得
    def get(self, request, *args, **kwargs):
        # Modelからすべての情報を取得
        sample_model_query = SampleModel.objects
        
        # item_nameでフィルタ
        item_name = request.GET.get("item_name")
        if item_name == None or item_name == "":
            # 検索条件が未指定の場合は全件表示
            sample_objects = sample_model_query.all()
        else:
            sample_objects = sample_model_query.filter(item_name=item_name).all()
        
        # Tableデータを生成
        table = SampleTable(sample_objects)
        
        # HTMLに出力する内容をセット
        context = {"table": table, 
                   "record_count": sample_objects.count()} # レコード件数
        
        # HTMLを出力
        return render(request, self.template_name, context)
        
   


