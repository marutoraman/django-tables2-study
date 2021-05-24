from django.shortcuts import render
from django.views import generic
from django.contrib import messages 

from ..forms.search_word import *
from ..models.search_word import *


# キーワード・URL設定画面　キーワード設定画面
class SearchWordView(generic.TemplateView):
    template_name = "setting/search_word.html"
    form_class = "SearchWordForm"

    def get(self, request, *args, **kwargs):
        # ライセンス確認
        if request.user.plan not in ["ALL_PLAN","WORD_PLAN"]:
            messages.warning(self.request, 'キーワード登録機能は、現在のライセンスでは使用できません。管理者に連絡してください。')
            return render(request,  "setting/search_word.html")
        
        # ラクマ、メルカリの切り替え
        if request.path.find("rakuma") >= 0:
            self.template_name = "setting/search_word_rakuma.html"
            search_words = SearchWordModel.objects.filter(account_id=self.request.user, search_site="rakuma", is_completed=False)
        else :
            self.template_name = "setting/search_word.html"
            search_words = SearchWordModel.objects.filter(account_id=self.request.user, search_site="mercari", is_completed=False)
            
        if int(search_words.count()) >= 1:  
            word_list = ""
            for word in search_words:
                word_list+=word.search_word + "\n"

            # 末尾改行削除
            word_list = word_list.rstrip('\n')
            # formにセット
            print(search_words[0].max_page_num,flush=True)
            data = dict(search_words=word_list,max_page_num=search_words[0].max_page_num)
            form = SearchWordForm(initial=data)
            
            return render(request, self.template_name, {'form': form})

        # 対象ユーザーにキーワードが無い場合は新規登録
        form = SearchWordForm()
        return render(request,  self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        登録ボタン押下時
        '''
        params = {'result': '', 'form': None}
        form = SearchWordForm(request.POST)
        if form.is_valid():
            if request.path.find("rakuma") >= 0:
                # チェックでエラーがない場合データを更新
                words = SearchWordModel.objects.filter(account_id=self.request.user, search_site="rakuma", is_completed=False)
                search_site = "rakuma"
                self.template_name = "setting/search_word_rakuma.html"
            else:
                words = SearchWordModel.objects.filter(account_id=self.request.user, search_site="mercari", is_completed=False)
                search_site = "mercari"
                self.template_name = "setting/search_word.html"
            words.delete()

            search_words = request.POST['search_words']
            max_page_num = request.POST['max_page_num']
            if len(search_words) != 0:
                search_words = search_words.split('\n')
                search_words = list(filter(lambda a: a != '', search_words))
                for search_word_value in search_words:
                    k = SearchWordModel(account_id=request.user, 
                                        search_word=search_word_value, search_site=search_site,
                                        max_page_num=max_page_num)
                    k.save()

            params["result"] = "{}件".format(len(search_words))

        params['form'] = form

        return render(request, self.template_name, params)

