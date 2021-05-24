from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from setting.models.replace_word import *
from setting.forms.replace_word import *
from django.contrib.auth import get_user_model
from io import TextIOWrapper, StringIO, BytesIO
from csv import reader
User = get_user_model()

class ReplaceWordView(generic.TemplateView):
    template_name = "setting/replace_word.html"

    def get(self, request, *args, **kwargs):
        replace_word_obj = ReplaceWordModel.objects.filter(account_id=self.request.user).all()
        csv_upload_form = ReplaceWordCSVUploadForm()
        return render(request, self.template_name, {'replace_word_obj': replace_word_obj, 'form':csv_upload_form})
    
    def post(self, request, *args, **kwargs):
        base_words = request.POST.getlist("base_word")
        replace_words = request.POST.getlist("replace_word")
        # 既存のデータを一旦削除して、改めて登録
        ReplaceWordModel.objects.filter(account_id=self.request.user).delete()
        objects=[]
        index = 1
        for base_word,replace_word in zip(base_words,replace_words):
            # チェックボックスはoffの場合にPostされない仕様のため個々にnameを振り対処する
            is_alert = bool(request.POST.get(f"is_alert_{index}",False))
            objects.append(ReplaceWordModel(account_id=self.request.user, base_word=base_word, replace_word=replace_word, is_alert=is_alert))
            index += 1
        ReplaceWordModel.objects.bulk_create(objects)
        
        
        # CSVインポートする場合
        if "import-csv" in request.POST:
            try:
                csv_data = TextIOWrapper(request.FILES['input-file'].file, encoding='utf-8_sig')
                
                # 更新用のobjectを作成してBulkUpdate
                replace_word_objects = []
                for i,row in enumerate(csv_data):
                    if i == 0:
                        continue
                    values = row.split(",")
                    if len(values) != 3:
                        continue
                    replace_word_objects.append(ReplaceWordModel(
                        account_id = request.user,
                        base_word = values[0],
                        replace_word = values[1],
                        is_alert = False if values[2].replace("\n","") != "ON" else True
                    ))
                ReplaceWordModel.objects.bulk_create(replace_word_objects)
            except:
                messages.warning(request,"CSVがインポートできませんでした")
        
        elif "delete-all" in request.POST:
            ReplaceWordModel.objects.filter(account_id=self.request.user).delete()
        
        csv_upload_form = ReplaceWordCSVUploadForm()
        objects = ReplaceWordModel.objects.filter(account_id=self.request.user).all()
        
        return render(request, self.template_name, {'replace_word_obj': objects, 'form':csv_upload_form})
