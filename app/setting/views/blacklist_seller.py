from django.shortcuts import render
from django.views import generic

from ..forms.blacklist_seller import *
from ..models.blacklist_seller import *


# キーワード・URL設定画面　キーワード設定画面
class BlacklistSellerView(generic.TemplateView):
    template_name = "setting/blacklist_seller.html"
    form_class = "BlacklistSellerForm"

    def get(self, request, *args, **kwargs):
        # 検索
        blacklist_sellers = BlacklistSellerModel.objects.filter(account_id=self.request.user)

        if int(blacklist_sellers.count()) >= 1:  
            seller_list = ""
            for seller in blacklist_sellers:
                seller_list+=seller.seller_name + "\n"

            # 末尾改行削除
            seller_list = seller_list.rstrip('\n')
            # formにセット
            data = dict(blacklist_sellers=seller_list)
 
            form = BlacklistSellerForm(initial=data)

            return render(request, self.template_name, {'form': form})

        # 対象ユーザーにNGワードが無い場合は新規登録
        form = BlacklistSellerForm()
        return render(request,  self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        登録ボタン押下時
        '''
        params = {'result': '', 'form': None}
        form = BlacklistSellerForm(request.POST)
        if form.is_valid():
            # チェックでエラーがない場合データを更新
            sellers = BlacklistSellerModel.objects.filter(account_id=self.request.user)
            sellers.delete()

            blacklist_sellers= request.POST['blacklist_sellers']
            if len(blacklist_sellers) != 0:
                blacklist_sellers = blacklist_sellers.split('\n')
                blacklist_sellers = list(filter(lambda a: a != '', blacklist_sellers))
                for seller_name in blacklist_sellers:
                    k = BlacklistSellerModel(account_id=request.user, 
                            seller_name=seller_name)
                    k.save()
                    BlacklistSellerModel.objects.all()

            params["result"] = "{}件".format(len(blacklist_sellers))

        params['form'] = form

        return render(request, self.template_name, params)

