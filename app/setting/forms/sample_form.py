from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.fields import ChoiceField
from django.forms import TextInput
from ..models.sample_form import *

class SampleForm(forms.ModelForm):
    '''
    このサンプルは、ヤフオクの出品情報を定義するためのもので、実案件のものを流用しています。
    ModelFormクラスを継承した場合は、ModelとFormが1対1で紐づく前提となる。
    画面-Form-Modelが1対1の関係の場合は、FormModelを使用すると実装が楽。
    一方、検索フォーム等のViewに情報を渡すことのみを目的としたModelを伴わないFormの場合は
    forms.Fromクラスを使用する。
    '''
    # MetaはForm全体に関わる定義情報を記述
    class Meta():
        model=SampleModel # modelとの紐付け
        # 表示させる項目、順番を定義(modelのカラム名で指定)
        fields=('auction_mode','units','kaisai_kikan','end_time','shipping_address','souryou_futan',
                'item_condition','hyouka_seigen','bad_hyouka_seigen','nyuusatsusya_ninsyou_seigen','auto_extention',
                'fast_end','auto_saisyuppin','shipping_date','other_shipping_method','other_shipping_price','description_template',
                'syuppin_sleep_sec')
        
        # 特定の項目に特別な属性を付与する場合の指定
        widgets = {
            # テキストエリアのサイズ変更
            'description_template': forms.Textarea(attrs={'rows':20, 'cols':80})
        }