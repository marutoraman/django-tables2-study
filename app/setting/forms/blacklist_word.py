from django import forms

class BlackListWordForm(forms.Form):
    blacklist_words = forms.CharField(label='NGワードを複数登録', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))