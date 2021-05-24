from django.contrib import admin
from setting.models.syuppin_column_config import *
# Register your models here.

@admin.register(SyuppinColumnConfigModel)
class AdminSyuppinColumnConfig(admin.ModelAdmin):
    list_display = ('syuppin_column_id', 'excel_column_id')