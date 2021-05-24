from django.urls import path
from .views.asin import *
from .views.asin_group import *
from .views.price_setting import *
from .views.exclude_asin import *
from .views.exclude_word import *
from .views.common_setting import *
from .views.eval_setting import *
from .views.search_word import *
from .views.blacklist_word import *
from .views.blacklist_seller import *
from .views.fetch_url import *
from .views.profit import *
from .views.replace_word import *
from .views.sample_form import *

app_name = 'setting'
urlpatterns = [
    path('asin', AsinView.as_view(), name="asin"),
    path('price-setting', PriceSettingView.as_view(), name="price-setting"),
    path('replace-word', ReplaceWordView.as_view(), name="replace-word"),
    path('exclude-asin', ExcludeAsinView.as_view(), name="exclude-asin"),
    path('exclude-word', ExcludeWordView.as_view(), name="exclude-word"),
    path('common-setting',SyuppinCommonSettingView.as_view(), name="common-setting"),
    path('eval-setting',EvalSettingView.as_view(), name="eval-setting"),
    path('search-word',SearchWordView.as_view(), name="search-word"),
    path('search-word-rakuma',SearchWordView.as_view(), name="search-word-rakuma"),
    path('blacklist-word',BlacklistWordView.as_view(), name="blacklist-word"),
    path('blacklist-seller',BlacklistSellerView.as_view(), name="blacklist-seller"),
    path('fetch-url',FetchUrlView.as_view(), name="fetch-url"),
    path('profit', ProfitView.as_view(), name="profit"),
    path('sample', SampleFormView.as_view(), name="sample"),
]