import django_tables2 as tables
from django.utils.html import mark_safe
from django_tables2.utils import Accessor
from setting.models.asin_group import *


class MaterializeCssCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox",
                   "name": bound_column.name, "value": value, }
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(
            default, **(specific or general or {}))
        return mark_safe("<p><label><input %s/><span></span></label></p>" % attrs.as_html())


class StatusViewTable(tables.Table):
    checkbox = MaterializeCssCheckboxColumn(accessor='pk')
    asin_group_id = tables.TemplateColumn(
        '{% if not record.started_at %}\
            <a href="/setting/asin?asin_group_id={{record.asin_group_id}}&yahoo_account_id={{record.yahoo_account_id}}">{{record.asin_group_id}}</a>\
         {% else %}\
            {{record.asin_group_id}}\
         {% endif %}', 
        verbose_name='ASINグループID')
    count_container = tables.TemplateColumn(
        '<div>{{record.completed_count}} / {{record.asin_count}}件</div>',
        verbose_name = "完了数 / ASIN登録件数",
        orderable = False
    )
    class Meta:
        model = AsinGroupModel
        template_name = 'django_tables2/bootstrap4.html'

        fields = ('checkbox','yahoo_account_id','asin_group_id','count_container','created_at','started_at','completed_at')
