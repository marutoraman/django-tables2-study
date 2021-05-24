from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.fields import ChoiceField
from django.forms import TextInput
from ..models.common_setting import *

class SyuppinCommonSettingForm(forms.ModelForm):
    
    class Meta():
        model=SyuppinCommonSettingModel    
        fields=('sec_no', 'column_id', 'column_name', 'column_value', 'updated_at')