import logging
import django_tables2 as tables
from django.utils.html import mark_safe
from django_tables2.utils import Accessor
from ..models.common_setting import *
from syuppin.tables.common import *
from config.const import *

class SyuppinCommonSettingTable(tables.Table):
    column_id = tables.TemplateColumn('<div><input type="hidden" name="column_id" value="{{record.column_id}}">{{record.column_id}}</div>',
                                      attrs={"th": {"class": "table-col-1"}})
    column_name = tables.Column(attrs={"th": {"class": "table-col-2"}})
    column_value = tables.TemplateColumn(
         '<div class="syuppin-price"><input class="form-control" type="text" name="column_value" value="{{record.column_value}}" /></div>',
          attrs={"th": {"class": "table-col-5"}},
          verbose_name="設定値"
    )
    delete = tables.TemplateColumn(
         '<button name="delete" class="ml-1 btn btn-light" value="{{record.pk}}">\
            <i class="fas fa-trash-alt fa-lg delete-icon"></i>\
          </button>',
          attrs={"th": {"class": "table-col-1"}},
          verbose_name=""
    )

    
    class Meta:
        model = SyuppinCommonSettingModel
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        
        fields = ('column_id', 'column_name','column_value', 'delete') 
        # 行単位でユニークなIDを付与
        row_attrs = {
            "name"   : "item_row",
            "data-id": lambda record: record.pk,
            "class" : "align-middle"
        }

