import logging
import django_tables2 as tables
from django.utils.html import mark_safe
from django_tables2.utils import Accessor
from ..models.syuppin import *
from .common import *
from config.const import *

class SyuppinItemTable(tables.Table):
    checkbox = MaterializeCssCheckboxColumn(accessor='pk',verbose_name="")
    row_no = tables.TemplateColumn("""
                                   <button name="delete_row" class="ml-1 btn btn-light" value="{{record.pk}}">
                                        <i class="fas fa-trash-alt fa-lg delete-icon"></i>
                                    </button>
                                    <input type="hidden" name="pk" value="{{record.pk}}" />
                                   """,
                                   verbose_name="No")
    # f文字列との併用はできないためformatで埋め込む
    
    image_container = tables.TemplateColumn(
        """
        <label class="image-selector pull-left ml-0">\
        <input type="checkbox" name="is_image1_selected" class="hidden-checkbox" value="{{record.is_image1_selected}}" {{record.is_image1_selected}}>\
        <img class="img-thumbnail table-image target-image" src="{{record.thumbnail_url}}"/>\
        </label>\
        <div class="row">\
        {% if record.image_url2 %}\
            <label class="image-selector">\
            <input type="checkbox"  name="is_image2_selected" class="hidden-checkbox" {{record.is_image2_selected}}>\
            <img class="img-thumbnail small-image target-image2" src="{{record.image_url2}}"/>\
            </label>\
        {% endif %}\
        {% if record.image_url3 %}\
            <label class="image-selector">\
            <input type="checkbox"  name="is_image3_selected" class="hidden-checkbox" {{record.is_image3_selected}}>\
            <img class="img-thumbnail small-image target-image2" src="{{record.image_url3}}"/>\
            </label>\
        {% endif %}\
        {% if record.image_url4 %}\
            <label class="image-selector">\
            <input type="checkbox"  name="is_image4_selected" class="hidden-checkbox" {{record.is_image4_selected}}>\
            <img class="img-thumbnail small-image target-image2" src="{{record.image_url4}}"/>\
            </label>\
        {% endif %}\
        {% if record.image_url5 %}\
            <label class="image-selector">\
            <input type="checkbox"  name="is_image5_selected" class="hidden-checkbox" {{record.is_image5_selected}}>\
            <img class="img-thumbnail small-image target-image2" src="{{record.image_url5}}"/>\
            </label>\
        {% endif %}
        </div>
        """,
        verbose_name='')

    item_info_container = tables.TemplateColumn(
         '{% if record.is_alert == 1 %}\
            <i class="fas fa-exclamation-triangle fa-2x alert-icon mb-2"></i>\
          {% endif %}\
          {% if record.site == "mercari" %}\
            <a href="{{record.url}}" target="_blank"><div class="mercari-icon">　</div></a>\
          {% elif record.site == "rakuma" %}\
            <a href="{{record.url}}" target="_blank"><div class="rakuma-icon">　</div></a>\
          {% endif %}\
          <a href="{{record.url}}" target="_blank">商品ページへ</a>\
          <div><input class="form-control item-field" name="item_name" type="text" value="{{record.item_name}}" /></div>\
          <div><span>【出品者】{{record.seller_name}}</span><span class="ml-2">【状態】{{record.condition}}</span></div>\
          <div>(id: {{record.item_id}})</div>',
          verbose_name="商品情報"
    )
    
    price_container = tables.TemplateColumn(
        '<div class="price-field">\
            <div>販売価格:<input class="form-control" name="amazon_price" type="number" value="{{record.amazon_price}}" /></div>\
            <div class="amazon-price">仕入価格:￥ {{record.price}}</div>\
            <div>({{record.shipping_payment}})</div>\
        </div>',
        verbose_name="価格"
    )
    
    
    # description = tables.TemplateColumn(
    #     '<div class="description-field"><textarea rows="5" class="form-control" name="description">{{record.description}}</textarea></div>',
    #     verbose_name="商品説明"
    # )
    
    # delete_btn =  tables.TemplateColumn(
    #     """
    #     <button name="delete" class="ml-1 btn btn-light" value="{{profit_value.pk}}">\
    #         <i class="fas fa-trash-alt fa-lg delete-icon"></i>
    #     </button>
    #     """,
    #     verbose_name=""
    # )
    
    class Meta:
        model = SyuppinItemModel
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        
        fields = ('checkbox', 'row_no', 'image_container', 'item_info_container', 
                  'price_container') 
        # 行単位でユニークなIDを付与
        row_attrs = {
            "name"   : "item_row",
            "data-id": lambda record: record.pk,
            #"class" : lambda record: f"align-middle {'is-alert-row' if record.is_alert else ''}" # アラート行は強調する
            "class" : "align-middle" 
        }

