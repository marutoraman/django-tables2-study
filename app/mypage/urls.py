from django.urls import path
from .views.mypage import *
from .views.logout import *
from .views.manual import *
from .views.yahoo_account import *

app_name = 'mypage'
urlpatterns = [
    path('mypage', MyPageView.as_view(), name="mypage"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('manual', ManualView.as_view(), name="manual"),
    path('yahoo_account', YahooAccountView.as_view(), name="yahoo_account"),

]