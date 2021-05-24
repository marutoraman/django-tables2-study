from django.urls import path
from .views.syuppin import *
from .views.status import *

app_name = 'syuppin'
urlpatterns = [
    path('status', StatusView.as_view(), name="status"),
    path('list', SyuppinItemView.as_view(), name="list"),

]