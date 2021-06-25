import logging
import django_tables2 as tables
from django.utils.html import mark_safe
from django_tables2.utils import Accessor
from ..models.sample import *
from config.const import *

class SampleTable(tables.Table):

    class Meta:
        model = SampleModel
        template_name = 'django_tables2/bootstrap4.html'
        
        fields = ('item_name', 'item_id', 'description', 'price') 


