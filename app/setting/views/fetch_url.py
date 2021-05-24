from django.shortcuts import render
from django.views import generic
from django.contrib import messages 

from ..forms.fetch_url import *
from ..models.fetch_url import *

# URL設定画面
class FetchUrlView(generic.TemplateView):
    template_name = "setting/fetch_url.html"
    form_class = "FetchUrlsForm"

    def get(self, request, *args, **kwargs):
        # ライセンス確認
        if request.user.plan not in ["ALL_PLAN","URL_PLAN"]:
            messages.warning(self.request, 'URL登録機能は、現在のライセンスでは使用できません。管理者に連絡してください。')
            return render(request,  "setting/fetch_url.html")
            
        # 検索
        fetch_urls = FetchUrlModel.objects.filter(account_id=self.request.user, is_completed=False)

        if int(fetch_urls.count()) >= 1:  
            url_list = ""
            for url in fetch_urls:
                url_list+=url.url + "\n"

            # 末尾改行削除
            url_list = url_list.rstrip('\n')
            data = dict(urls = url_list)
            # formにセット
            form = FetchUrlsForm(initial=data)

            return render(request, self.template_name, {'form': form})
        
        # 対象ユーザに登録済みURLが無い場合は新規登録
        form = FetchUrlsForm()
        return render(request,  self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        登録ボタン押下時
        '''
        params = {'result': '', 'form': None}
        form = FetchUrlsForm(request.POST)
        if form.is_valid():
            # チェックでエラーがない場合データを更新
            fetch_urls = FetchUrlModel.objects.filter(account_id=self.request.user)
            fetch_urls.delete()

            urls = request.POST['urls']
            if len(urls) != 0:
                urls = request.POST['urls'].split('\n')
                urls = list(filter(lambda a: a != '', urls))
                for url_value in urls:
                    k = FetchUrlModel(account_id=request.user, 
                            url=url_value)
                    k.save()
                    FetchUrlModel.objects.all()

            params["result"] = "{}件".format(len(urls))

        params['form'] = form

        return render(request, self.template_name, params)
    
    

