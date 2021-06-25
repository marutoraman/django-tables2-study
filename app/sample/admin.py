from .models.sample import SampleModel
from django.contrib import admin

# Register your models here.
@admin.register(SampleModel)
class AdminSampleConfig(admin.ModelAdmin):
    list_display = ('item_name', 'price')