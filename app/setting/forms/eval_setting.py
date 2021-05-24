from django import forms
from django.forms import fields
from .asin import *
from ..models.eval_setting import *

class EvalSettingForm(forms.ModelForm):
    yahoo_account_id = forms.fields.ChoiceField(
        required=True,
        widget=forms.widgets.Select,
        label="ヤフオクID"
    )
    eval_message = forms.CharField(label='評価メッセージ', required=True, 
                                    widget=forms.Textarea(attrs={
                                        'class': 'textarea-small form-control'
                                        }))
    
    class Meta():
        model=EvalSettingModel
        fields=('yahoo_account_id', 'eval_message')