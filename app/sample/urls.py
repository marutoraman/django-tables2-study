from django.urls import path
from .views.sample import *

app_name = 'sample'
urlpatterns = [
    path('list', SampleView.as_view(), name="list"),

]