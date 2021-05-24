from django import forms
from config.const import *

class SearchWordForm(forms.Form):
    max_page_num = forms.ChoiceField(label='最大ページ数', choices=SELECTION.MAX_PAGE_NUM, required=True)
    search_words = forms.CharField(label='キーワードを複数登録', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))