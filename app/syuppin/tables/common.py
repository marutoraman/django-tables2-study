import django_tables2 as tables
from django.utils.html import mark_safe

class MaterializeCssCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "class":"table-checkbox-scale",
                   "name": bound_column.name, "value": value, }
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(
            default, **(specific or general or {}))
        return mark_safe("<p><label class='table-checkbox'><input %s/><span></span></label></p>" % attrs.as_html())

# CheckbokColumnクラスを改造してBotton用にする
class MaterializeCssButtonColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        # モーダル専用
        default = {"type": "button", "name": bound_column.name, "data-id": value, "value": "編集",
                   "class": "btn btn-primary", "data-toggle": "modal", "data-target": "#exampleModal"}
        # if self.is_checked(value, record):
        #    default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(
            default, **(specific or general or {}))
        return mark_safe("<p><label><input %s/><span></span></label></p>" % attrs.as_html())

# CheckbokColumnクラスを改造してinput用にする
class MaterializeCssTextColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        # モーダル専用
        # logging.debug(bound_column.innerText)
        default = {"type": "text", "name": bound_column.name, "data-id": value}
        # if self.is_checked(value, record):
        #    default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(
            default, **(specific or general or {}))
        return mark_safe("<p><label><input %s/><span></span></label></p>" % attrs.as_html())