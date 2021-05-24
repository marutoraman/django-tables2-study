from django import forms
from .asin import *

class ExclusionAsinsForm(forms.Form):
    asins = AsinsField(label='除外ASIN一覧', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))