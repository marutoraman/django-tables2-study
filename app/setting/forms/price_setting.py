from django import forms
from ..models.price_setting import *

class PriceSettingForm(forms.ModelForm):
    yahoo_account_id = forms.fields.ChoiceField(
        required=True,
        widget=forms.widgets.Select
    )
        
    class Meta():
        model = PriceSettingModel
        fields=('yahoo_account_id',
                'price_range1','price_rate1','price_range2','price_rate2',
                'price_range3','price_rate3','price_range4','price_rate4',
                'price_range5','price_rate5','sokketsu_price_offset')
