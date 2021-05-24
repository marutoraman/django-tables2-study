from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.contrib import messages
from django_tables2 import SingleTableView, RequestConfig
from users.models import User,YahooAccount
from ..models.eval_setting import *
from ..forms.eval_setting import *
from django.contrib.auth import get_user_model
User = get_user_model()


class EvalSettingView(generic.FormView):
    template_name="setting/eval_setting.html"
    form_class=EvalSettingForm

    def get(self, request, *args, **kwargs):
        # フォームに入力した値をDBに保存する
        if request.GET.get('yahoo_account_id') != None:
            setting = EvalSettingModel.objects.filter(account_id=self.request.user, 
                                                        yahoo_account_id=request.GET.get('yahoo_account_id')).first()
        else:
            setting = EvalSettingModel.objects.filter(account_id=self.request.user).first()
        if setting == None:
            setting = EvalSettingModel(account_id=self.request.user)

        form = self.create_form(setting)

        return render(request, self.template_name, {'form': form,})

    def post(self, request, *args, **kwargs):
        # フォームに入力した値をDBに保存する
        setting = EvalSettingModel.objects.filter(account_id=self.request.user, 
                                                   yahoo_account_id=request.POST['yahoo_account_id']).first()
        # 新規の場合はCreate
        if setting == None:
            setting = EvalSettingModel(account_id=self.request.user, 
                                        yahoo_account_id=request.POST['yahoo_account_id'])
        form = self.create_form(setting)
        form.save()
        
        return render(request, self.template_name, {'form': form})
    
    def create_form(self, setting):
        '''
        ドロップダウンにヤフオクアカウントをセットしたフォームを作成する
        '''
        # GETの場合
        if self.request.method == "GET" and self.request.GET.get('yahoo_account_id'):
            form = EvalSettingForm(instance=setting, 
                                    initial={'yahoo_account_id':self.request.GET.get('yahoo_account_id')})
        # POSTの場合
        elif self.request.method == "POST" and self.request.POST.get('yahoo_account_id'):
            form = EvalSettingForm(self.request.POST, instance=setting, 
                                    initial={'yahoo_account_id':self.request.POST.get('yahoo_account_id')})
        # yahoo_account_idが存在しない場合
        else:
            form = EvalSettingForm(instance=setting)
            
        # ヤフオクIDを取得
        user_obj = User.objects.filter(account_id=self.request.user).first()
        # ヤフオクカウントIDをFormにセット
        form.fields['yahoo_account_id'].choices=[
            (obj.yahoo_account_id, obj.yahoo_account_id) for obj in user_obj.yahoo_account_id.all()
        ]
        
        return form