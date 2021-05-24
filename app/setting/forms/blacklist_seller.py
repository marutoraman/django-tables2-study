from django import forms

class BlacklistSellerForm(forms.Form):
    blacklist_sellers = forms.CharField(label='除外セラーを複数登録', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))