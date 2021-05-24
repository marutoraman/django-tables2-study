from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from users.models import YahooAccount 
from django.contrib.auth import get_user_model
User = get_user_model()

class YahooAccountView(generic.TemplateView):
    template_name = "mypage/yahoo_account.html"

    def get(self, request, *args, **kwargs):
        user_obj = User.objects.filter(account_id=self.request.user).first()

        return render(request, self.template_name, {'yahoo_account_obj': user_obj.yahoo_account_id.all()})
    
    def post(self, request, *args, **kwargs):
        yahoo_account_ids = request.POST.getlist("yahoo_account_id")
        yahoo_passes = request.POST.getlist("yahoo_pass")

        # 既存のヤフオクID情報を取得
        user_obj = User.objects.filter(account_id = request.user).first()
        yahoo_account_obj = user_obj.yahoo_account_id.all()
        for yahoo_account_id,password in zip(yahoo_account_ids,yahoo_passes):
            # update
            for yahoo_account in yahoo_account_obj:
                if yahoo_account.yahoo_account_id == yahoo_account_id:
                    yahoo_account.yahoo_pass=password
                    yahoo_account.save()
                    break
            # insert
            else:
                # ManytoManyのInsertのため始めにYahooAccountを追加してから、その情報をUserに追加する
                obj = YahooAccount(yahoo_account_id=yahoo_account_id, yahoo_pass=password)
                obj.save()
                user_obj.yahoo_account_id.add(obj)
                
        return render(request, self.template_name, {'yahoo_account_obj': user_obj.yahoo_account_id.all()})

    # def post(self, request, *args, **kwargs):
    #     # フォームに入力した値をDBに保存する
    #     setting = PriceSettingModel.objects.filter(account_id=self.request.user, 
    #                                                yahoo_account_id=request.POST['yahoo_account_id']).first()
    #     # 新規の場合はCreate
    #     if setting == None:
    #         setting = PriceSettingModel.objects.create(account_id=self.request.user, 
    #                                                    yahoo_account_id=request.POST['yahoo_account_id'])
    #     form = self.create_form(setting)
    #     form.save()
        
    #     return render(request, self.template_name, {'form': form})