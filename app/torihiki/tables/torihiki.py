import logging
import django_tables2 as tables
from django.utils.html import mark_safe
from django_tables2.utils import Accessor
from ..models.torihiki import *
from syuppin.tables.common import *
from config.const import *

class TorihikiTable(tables.Table):
    checkbox = MaterializeCssCheckboxColumn(accessor='pk',verbose_name="")

    item_name = tables.TemplateColumn(
        '<div class="item-field">{{ record.item_name }}</div>',
         verbose_name="商品名"
    )
    
    execute_shipping = tables.TemplateColumn(
        '{% if record.shipping_notice_stat == 0 %}\
            <input name="execute_shipping" type="button" class="btn btn-primary" data-shipping="{{ record.shipping_data }}" data-asin="{{ record.asin }}" value="仕入れ"/>\
         {% else %}\
            <input name="execute_shipping" type="button" class="btn btn-secondary" data-shipping="{{ record.shipping_data }}" data-asin="{{ record.asin }}" value="仕入れ" disabled/>\
         {% endif %}',
         verbose_name=""
    )
    
    amazon_link_btn = tables.TemplateColumn(
        '{% if record.asin %}\
            <a name="amazon_url" href="https://www.amazon.co.jp/dp/{{ record.asin }}" target="_blank"><inputtype="button" class="btn btn-secondary" />Amazon</a>\
         {% endif %}',
         verbose_name=""
    )
    
    profit = tables.TemplateColumn(
        '{% if record.profit %}\
            <div>{{ record.profit }}</div>\
         {% endif %}',
         verbose_name="利益"
    )
    
    eval_stat = tables.TemplateColumn(
        '<div class="eval-stat-{{record.eval_stat}}"></div>',
        verbose_name=""
    )
    
    class Meta:
        model = TorihikiModel
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        fields = ('checkbox', 'item_name', 
                  'buied_price', 'amazon_price', 'profit', 'execute_shipping', 
                  'amazon_link_btn','eval_stat','rakusatsu_at','shipped_at',
                  'eval_at','completed_at') 
        # 行単位でユニークなIDを付与
        row_attrs = {
            "name"   : "item_row",
            "data-id": lambda record: record.pk,
            "class" : "align-middle"
        }

