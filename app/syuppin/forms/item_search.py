from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.fields import ChoiceField
from django.forms import TextInput

class ItemSearchForm(forms.Form):

    # Amazon本体
    SELL_AMAZON_CHOICE = {
        ('0', 'すべて'), # 0だと画面先頭に表示されないので000にしています。
        ('1', 'なし'),
        ('2', 'あり'),
    }
    sell_amazon = forms.ChoiceField(label='Amazon販売', 
                                    widget=forms.RadioSelect, choices=SELL_AMAZON_CHOICE, initial=0)

    # カート価格 下限
    cart_price_label = forms.CharField(label="カート価格")
    cart_price_min = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Min',
                                        'pattern': '^[0-9]+$'}))
    cart_price_max = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Max',
                                        'pattern': '^[0-9]+$'}))
    # 90日なし率
    non_amazon_90days_label = forms.CharField(label="90日なし率")
    non_amazon_90days_min = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Min',
                                        'pattern': '^[0-9]+$'}))
    non_amazon_90days_max = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Max',
                                        'pattern': '^[0-9]+$'}))

    # 単品利益
    profit_label = forms.CharField(label="利益")
    profit_min = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Min',
                                        'pattern': '^[0-9]+$'}))
    profit_max = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Max',
                                        'pattern': '^[0-9]+$'}))

    # 利益率 下限・上限
    profit_rate_label = forms.CharField(label="利益率")  # maxlength値は？
    profit_rate_min = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Min',
                                        'pattern': '^[0-9]+$'}))
    profit_rate_max = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Max',
                                        'pattern': '^[0-9]+$'}))

    SINGLE_CHOICE = [(True, "")]
    item_quantity_exclusion = forms.MultipleChoiceField(
        label="セット商品除外",
        required=False,
        disabled=False,
        initial=[],
        choices=SINGLE_CHOICE,
        widget=forms.CheckboxSelectMultiple(attrs={}))
