from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from users.models import YahooAccount
from setting.models.common_setting import * 
from setting.models.profit import * 
from django.contrib.auth import get_user_model
User = get_user_model()

class MyPageView(generic.TemplateView):
    template_name = "mypage/mypage.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(account_id=request.user).first()
        self.create_init_table()
        return render(request, self.template_name, {'user': user})
    
    def create_init_table(self):
        '初回ログイン時限定で、各種テーブルを作成'
        # 出品共有項目設定
        obj = SyuppinCommonSettingModel.objects.filter(account_id=self.request.user).first()
        if obj == None:
            objects = SyuppinCommonSettingModel.objects.filter(account_id="__default__").all()
            setting_objects = []
            for obj in objects:
                setting_obj = SyuppinCommonSettingModel(account_id=self.request.user, sec_no=obj.sec_no, 
                                          column_id=obj.column_id, column_name=obj.column_name,
                                          column_value=obj.column_value)
                
                setting_objects.append(setting_obj)
            SyuppinCommonSettingModel.objects.bulk_create(setting_objects)
        
        # 利益設定
        obj = ProfitModel.objects.filter(account_id=self.request.user).first()
        if obj == None:
            ProfitModel.objects.create(account_id=self.request.user, seq_no=0, base_price=100000, profit=1000)
            