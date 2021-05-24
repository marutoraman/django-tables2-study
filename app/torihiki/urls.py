from django.urls import path
from .views.torihiki import *

app_name = 'torihiki'
urlpatterns = [
    path('list', TorihikiView.as_view(), name="list"),
]