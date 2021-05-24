from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from ..models.profit import *
from django.contrib.auth import get_user_model
from django.db.models import Max
User = get_user_model()

class ProfitView(generic.TemplateView):
    template_name = "setting/profit.html"

    def get(self, request, *args, **kwargs):
        profit_obj = ProfitModel.objects.filter(account_id=self.request.user).order_by('base_price')

        return render(request, self.template_name, {'profit_obj': profit_obj.all()})
    
    def post(self, request, *args, **kwargs):
        # 削除
        if request.POST.get("delete"):
            id = request.POST.get("delete")
            ProfitModel.objects.filter(account_id=self.request.user, pk=id).delete()
        # 登録
        else:
            ids = request.POST.getlist("setting_id")
            base_prices = request.POST.getlist("base_price")
            profits = request.POST.getlist("profit")

            # 既存の利益情報を取得
            profit_obj = ProfitModel.objects.filter(account_id=self.request.user).order_by('base_price')

            for base_price,profit,id in zip(base_prices,profits,ids):
                if base_price == "" or profit == "":
                    continue
                obj = ProfitModel.objects.filter(account_id=self.request.user, pk=id).first()
                # insert
                if obj == None:
                    obj = ProfitModel(account_id=request.user)
                # update
                obj.base_price = base_price
                obj.profit=profit
                obj.save()
        
        profit_obj = ProfitModel.objects.filter(account_id=self.request.user).order_by('base_price')
        return render(request, self.template_name, {'profit_obj': profit_obj.all()})