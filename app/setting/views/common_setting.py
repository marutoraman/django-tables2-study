from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.contrib import messages
from django_tables2 import SingleTableView, RequestConfig
from django.db.models import Max
from users.models import User,YahooAccount
from ..models.common_setting import *
from ..forms.common_setting import *
from ..tables.syuppin_common_setting import *
from django.contrib.auth import get_user_model
User = get_user_model()


class SyuppinCommonSettingView(generic.TemplateView):
    template_name="setting/common_setting.html"
    form_class=SyuppinCommonSettingForm

    def get(self, request, *args, **kwargs):
        return self.render_data(request)
    
    def post(self, request, *args, **kwargs):
        # 削除
        if request.POST.get("delete"):
            id = request.POST.get("delete")
            SyuppinCommonSettingModel.objects.filter(account_id=request.user, pk=id).delete()
            return self.render_data(request)
        
        # 追加        
        column_ids = request.POST.getlist("column_id")
        column_values = request.POST.getlist("column_value")
        add_column_id = request.POST.get("add_column_id")
        add_column_value = request.POST.get("add_column_value")
        add_column_name = request.POST.get("add_column_name")
        for column_id,column_value in zip(column_ids,column_values):
            obj = SyuppinCommonSettingModel.objects.filter(account_id=request.user, column_id=column_id).first()
            obj.column_value=column_value
            obj.save()
        
        if add_column_id != None and add_column_value != None and add_column_name != None\
           and add_column_name != "" and add_column_value != "" and add_column_name != "":
            try:
                # ID重複の場合はスキップ
                if SyuppinCommonSettingModel.objects.filter(account_id=request.user, column_id=add_column_id).first() != None:
                    return self.render_data(request)
                # sec_noの最大値+1で追加
                obj = SyuppinCommonSettingModel.objects.filter(account_id=request.user).order_by('-sec_no').first()
                SyuppinCommonSettingModel(account_id=request.user, sec_no = obj.sec_no+1,
                                          column_id=add_column_id, column_value=add_column_value, column_name=add_column_name).save()
            except:
                print("項目追加エラー",flush=True)
                
        return self.render_data(request)
    
    def render_data(self,request,**kwargs):
        # データ表示処理
        settings = SyuppinCommonSettingModel.objects.filter(account_id=request.user).order_by("sec_no").all()
        table = SyuppinCommonSettingTable(settings)
        context = {'table': table
                  }
        return render(request, self.template_name, context)
            