from django.shortcuts import render
from django.views import generic

from ..forms.blacklist_word import *
from ..models.blacklist_word import *


# キーワード・URL設定画面　キーワード設定画面
class BlacklistWordView(generic.TemplateView):
    template_name = "setting/blacklist_word.html"
    form_class = "BlackListWordForm"

    def get(self, request, *args, **kwargs):
        # 検索
        blacklist_words = BlacklistWordModel.objects.filter(account_id=self.request.user)

        if int(blacklist_words.count()) >= 1:  
            word_list = ""
            for word in blacklist_words:
                word_list+=word.blacklist_word + "\n"

            # 末尾改行削除
            word_list = word_list.rstrip('\n')
            # formにセット
            data = dict(blacklist_words=word_list)
 
            form = BlackListWordForm(initial=data)

            return render(request, self.template_name, {'form': form})

        # 対象ユーザーにNGワードが無い場合は新規登録
        form = BlackListWordForm()
        return render(request,  self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        登録ボタン押下時
        '''
        params = {'result': '', 'form': None}
        form = BlackListWordForm(request.POST)
        if form.is_valid():
            # チェックでエラーがない場合データを更新
            words = BlacklistWordModel.objects.filter(account_id=self.request.user)
            words.delete()

            blacklist_words= request.POST['blacklist_words']
            if len(blacklist_words) != 0:
                blacklist_words = blacklist_words.split('\n')
                blacklist_words = list(filter(lambda a: a != '', blacklist_words))
                for blacklist_word_value in blacklist_words:
                    k = BlacklistWordModel(account_id=request.user, 
                            blacklist_word=blacklist_word_value)
                    k.save()
                    BlacklistWordModel.objects.all()

            params["result"] = "{}件".format(len(blacklist_words))

        params['form'] = form

        return render(request, self.template_name, params)

