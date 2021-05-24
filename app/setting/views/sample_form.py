from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.contrib import messages
from django.db.models import Max
from users.models import User,YahooAccount
from ..models.sample_form import *
from ..forms.sample_form import *
from django.contrib.auth import get_user_model
User = get_user_model()


class SampleFormView(generic.TemplateView):
    template_name="setting/sample.html"
    form_class=SampleForm

    def get(self, request, *args, **kwargs):
        return self.render_data(request)
    
    def post(self, request, *args, **kwargs):
        setting = SampleModel.objects.filter(account_id=request.user).first()
        # レコードが存在しない場合は、新規作成
        if setting == None:
            setting = SampleModel(account_id=request.user)
            messages.success(request, "レコードを新規作成しました")

        # formからPOSTされたデータを読み込ませて、DBに簡単に保存できる
        form = SampleForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()   
            # メッセージ表示
            messages.success(request, "更新しました")
        else:
            messages.warning(request, "エラー")
            
        return self.render_data(request)
    
    def render_data(self,request,**kwargs):
        '''
        表示系の処理。GETでもPOSTでも共通して使用する
        '''
        # データ表示処理
        setting = SampleModel.objects.filter(account_id=request.user).first()
        # データをformに当てはめる
        if setting != None:
            form = SampleForm(instance=setting)
        else:
            form = SampleForm()
        context = {'form': form}
        
        return render(request, self.template_name, context)
            