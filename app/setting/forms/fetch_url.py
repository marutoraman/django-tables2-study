from django import forms
import re

class fetchUrlsField(forms.CharField):
    def clean(self, value):
        if len(value) == 0:
            # URL登録画面で0文字の場合、true
            # 入力必須の画面ではrequiredのため、0文字はあり得ない
            return super().clean(value)

        url_list = value.split("\r\n")

        #形式チェック
        type_message_array = []

        for url in url_list:
            # URLに使用できる文字か判定
            pattern = re.compile(r"^(http|https)://")
            m = pattern.match(url)
            
            if m is None:
                # 件数が多すぎると表示がおかしくなるのを考慮して10件
                if len(type_message_array) < 10:
                    type_message_array.append(url)
                    continue

        if len(type_message_array) > 0:
            message = "URLの入力形式が不正です（10件まで表示します）。{}".format(",".join(type_message_array))
            raise forms.ValidationError(message)
            
        return super().clean(value)

class FetchUrlsForm(forms.Form):
    urls = fetchUrlsField(label='URLを複数登録', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))

    # submitボタンの表示制御
    submit = "submit"