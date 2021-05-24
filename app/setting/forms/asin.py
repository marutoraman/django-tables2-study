from django import forms
import re
from config.const import *


class AsinsField(forms.CharField):
    def clean(self, value):
        if len(value) == 0:
            # 除外画面で0文字の場合、true
            # 入力必須の画面ではrequiredのため、0文字はあり得ない
            return super().clean(value)

        asin_list = value.split("\r\n")
        #件数チェック
        if len(asin_list) > SETTING.ASIN_MAX_LIMIT:
            raise forms.ValidationError('{}件以内で入力して下さい（入力件数{}）'.format(SETTING.ASIN_MAX_LIMIT, len(asin_list)) )

        #形式チェック
        type_message_array = []

        for asin in asin_list:
            # asin = asin.strip('\t').strip()
            m = re.fullmatch(r'^[0-9a-zA-Z]{10}', asin)
            if m is None:
                # 件数が多すぎると表示がおかしくなるのを考慮して10件
                if len(type_message_array) < 10:
                    type_message_array.append(asin)
                    continue
                    
            # if len(asin) != 10:
            #     if len(type_message_array) < 10:
            #         type_message_array.append(asin)

        if len(type_message_array) > 0:
            message = "ASINは半角英数10桁で入力して下さい（10件まで表示します）。{}".format(",".join(type_message_array))
            raise forms.ValidationError(message)
            
        return super().clean(value)

class AsinForm(forms.Form):
    asin_group_id = forms.CharField(label='ASINグループID',  max_length=100)
    asins = AsinsField(label='ASIN一覧', widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))
    yahoo_account_id = forms.fields.ChoiceField(
        label="ヤフオクID",
        required=True,
        widget=forms.widgets.Select
    ) 
      
    # submitボタンの表示制御
    submit = "submit"
    
    
    