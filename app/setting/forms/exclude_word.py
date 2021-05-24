from django import forms
from .asin import *

class ExclusionWordForm(forms.Form):
    word = forms.CharField(label='除外ワード', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))