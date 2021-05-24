from django.db.models.query import Prefetch
from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.contrib import messages
from ..models.asin import * 
from ..models.asin_group import *
from ..forms.asin import *
from django.contrib.auth import get_user_model
User = get_user_model()

# ASIN設定画面
class AsinView(generic.TemplateView):
    template_name = "setting/asin.html"
    form_class = "AsinForm"

    def get(self, request, *args, **kwargs):
        asin_group_id = None
        # ヤフオクIDを取得
        user_obj = User.objects.filter(account_id=self.request.user).first()
        if request.GET.get("asin_group_id"):
            asin_group_id = request.GET.get("asin_group_id")
        if asin_group_id != None:
            # getリクエストでasin_group_idが指定された場合は検索
            asin_group_id_obj=AsinGroupModel.objects.filter(account_id=self.request.user, asin_group_id=asin_group_id).first()
            # 該当するASIN設定一覧を取得
            if asin_group_id_obj != None:  
                asin_obj=AsinModel.objects.filter(account_id=self.request.user, asin_group_id_id=asin_group_id_obj.id)
                asins_str = ""
                # 1つのtextareaフィールドに全てのASINを改行して入れる
                for asin in asin_obj:
                    asins_str += asin.asin + "\n"
                # 末尾改行削除
                asins_str = asins_str.rstrip('\n')
                # formにセット
                data  = dict(asin_group_id=asin_group_id, asins=asins_str, 
                             yahoo_account_id=request.GET.get('yahoo_account_id'))
                form = AsinForm(initial=data)
                # ヤフオクカウントIDをFormにセット
                form.fields['yahoo_account_id'].choices=[
                    (obj.yahoo_account_id, obj.yahoo_account_id) for obj in user_obj.yahoo_account_id.all()
                ]
                
                return render(request, self.template_name, {'form': form})

        # getリクエストでasin_group_idが指定ない場合は新規登録
        form = AsinForm()
        # ヤフオクカウントIDをFormにセット
        form.fields['yahoo_account_id'].choices=[
            (obj.yahoo_account_id, obj.yahoo_account_id) for obj in user_obj.yahoo_account_id.all()
        ]

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # getリクエストでasin_group_idが指定された場合は検索
        user_obj = User.objects.filter(account_id=self.request.user).first()
        print(request.POST)
        asin_group_id = request.POST.get("asin_group_id")
        if asin_group_id == None:
            messages.warning(self.request, 'ASINグループIDが未設定です')
            return render(request, self.template_name, {'form': AsinForm()})
        
        # 修正の場合以外で既に存在する場合はエラー
        asin_group_id_obj=AsinGroupModel.objects.filter(account_id=self.request.user, asin_group_id=asin_group_id).first()
        # GETのasin_group_idが含まれる場合は修正からのPOSTのためID重複しても問題なし
        if asin_group_id_obj != None:
            if not request.GET.get("asin_group_id"):
                messages.warning(self.request, '同一のASINグループIDが存在します')
                return render(request, self.template_name, {'form': AsinForm()})
            else:
                # 存在する場合は一旦削除
                AsinGroupModel.objects.filter(account_id=self.request.user, asin_group_id=asin_group_id).delete()
                
        # ASIN追加
        asins = request.POST.get("asins")
        if len(asins) <= 2:
            messages.warning(self.request, 'ASINが未設定です。')
            return render(request, self.template_name, {'form': AsinForm()})
        asin_list = asins.split("\r\n")
        # 10文字以下は不正なASINなので削除
        for i,asin in enumerate(asin_list):
            if len(asin) < 10:
                asin_list.pop(i)
                
        asin_model_list=[]
        # アップデート
        asin_group_obj = AsinGroupModel(account_id=self.request.user, asin_group_id=asin_group_id, 
                                        yahoo_account_id=request.POST.get('yahoo_account_id'), asin_count=len(asin_list))
        asin_group_obj.save()
        for asin in asin_list:
            asin_model_list.append(AsinModel(asin=asin, account_id=self.request.user, asin_group_id=asin_group_obj)) #ForeiginKeyではModelobjectを渡す必要あり
        AsinModel.objects.bulk_create(asin_model_list)
        messages.success(self.request, '登録が完了しました。')

        # getリクエストでasin_group_idが指定ない場合は新規登録
        form = AsinForm()
        # ヤフオクカウントIDをFormにセット
        form.fields['yahoo_account_id'].choices=[
            (obj.yahoo_account_id, obj.yahoo_account_id) for obj in user_obj.yahoo_account_id.all()
        ]
        
        return render(request, self.template_name, {'form': form})
    
    

