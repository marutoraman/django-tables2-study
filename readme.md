実案件課題　メルカリ、ラクマ、Amazon物販業務効率化ツール
====
本タスクは、実際の案件の内容をタスク化した応用的なものです。  
Djangoの課題１～４およびその前提知識を習得していることを前提しておりますので、細かな機能の説明は省略しております。

この講座で扱うWebサイトの完成形は下記の動画を参照してください。  
https://youtu.be/7jiWb7vzoNE

## Django側の構築
### DockerでMySQLを構築、起動
dockerをインストールして、プロジェクトルートで以下コマンドを実行する。  
dockerのプロセスは常に起動した状態にする必要があるため、dockerコマンド実行後は  
別のターミナルを開いて作業を行う。  
```
docker-compose up --buld
```

### Python仮想環境の作成、ライブラリインストール、開発サーバー起動確認
venvを作成して有効化後、requirements.txtをinstall  
```
python -m venv venv
venv/Scripts/activate ※windows
. venv/bin/activate ※MacOS/Linux
pip install -r requirements.txt
```

開発用環境設定ファイル.env.devを.envにリネーム  
.env.dev →　.env  
※.envファイルを読み込むことで、開発環境と本番環境の差異を吸収する  
今回は、開発環境用の.envファイルのみを用意している。

初回migrationを実施して、superuserを作成、runserver起動確認
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 課題0:Djangoプロジェクト作成、アプリの作成
Djangoプロジェクトを任意の名称で作成し、以下の４つのアプリを作成します。  
settings.pyにもアプリ名を追記してください。  
```
mypage:マイページ関連
users:パスワード変更  
setting:設定関連（ASIN登録や除外設定など）  
syuppin:出品関連（商品一覧やExcel出力）  
```

### 各種フォルダの作成
以下のフォルダをプロジェクトルートに作成する。  
static:css/js等の静的ファイルを格納する  
templates:HTMLテンプレートファイルを格納する  
※アプリ毎に作成する方式もあるが、プロジェクトルートに１つ作成する方が管理しやすいのでオススメ。

既定では、アプリ配下のtemplatesを参照するため、templatesの場所を以下のDIRSで指定することで変更する。  
settings.py
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # templateをプロジェクト直下に配置するための設定
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Bootstrapテンプレートを適用
案件では、顧客の要望に合わせて適切なテンプレートを使用します。  
特に要望がない場合は、常に共通で使うテンプレートを決めておくと、工数が削減できます。  
※最近のモダン開発では、BootstrapよりもTailwind等の方が自由度が高く好まれる傾向にありますが  
多少難易度が高いため、本講座ではBootstrapを使用します。

本講座では、以下のテンプレートを使用します。  
https://coliss.com/articles/build-websites/operation/work/free-admin-template-stisla.html

その他のテンプレートの一例）Bootstrap5  
Volt公式  
https://github.com/themesberg/volt-bootstrap-5-dashboard  
Dango用にカスタマイズした版  
https://github.com/marutoraman/django-bootrap-template


#### 課題1:base.htmlへのテンプレート組み込み
以下を参照して、１からbase.htmlにテンプレートを組み込んでください。  
案件では、基本的には過去案件のコピペが可能ですが、新規のテンプレートを適用する場合は  
以下の作業を行う必要があります。

- 以下からテンプレート一式ダウンロードする  
https://github.com/stisla/stisla

- モジュールのコピー  
assetsフォルダをtemplatesフォルダにコピーする

- base.htmlの作成  
ダウンロードしたファイルのpages/layout-default.htmlをtemplatesにコピーして、base.htmlにリネームする。

```
<section class="section">
```
の配下の要素を全て削除する。  
section内は具体的なページ毎のコンテンツに相当するため、baseに記述は不要。  
（sectionタグ自体は削除しない。sectionの中身(下層)の要素を削除するが、footer等を削除するわけでない）  

必要な外部リンクを記述する  
以下のように使用するCSSのCDNをbase.htmlのheadタグ内に記載する。  
（バージョンはその時期に合わせて適切に選択する）  
※本テンプレートのBootstrapバージョンは4である前提。  
簡単にするために公式で公開されているものは全てCDNで指定しているが  
ローカルにダウンロードした方が初期のパフォーマンスは早くなるの可能性があるので  
ローカルにダウンロードしても良い。  

css系(bootstrapとfontawesome)
```
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
    integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
```

javascript系(jquery、ajax、bootstrap)
```
  <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.nicescroll/3.7.6/jquery.nicescroll.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.min.js"></script>
```

公式がCDNで公開していないライブラリについては、ローカルにダウンロードして、staticでアクセスする。  
プロジェクト内にリンクしている箇所をstaticのタグで置き換える。  
これにより、staticが実際のPATHに置き換わるので、環境に関わらず動作する。  

base.htmlの一番上に以下を記載することで、staticという名前でstaticフォルダのpathが参照可能になる。
```
{% load static %}
```

base.htmlのheadに以下のassetsの情報を追記する。
```
  <link rel="stylesheet" href="{% static 'assets/css/style.css' %}">
  <link rel="stylesheet" href="{% static 'assets/css/components.css' %}">
```

base.htmlのbodyの下部に以下のassetsの情報を追記する。
```
   <script src="{% static 'assets/js/scripts.js' %}"></script>
   <script src="{% static 'assets/js/custom.js' %}"></script>
```


### 課題2:Templateのカスタマイズ
- base.htmlに対して以下のように、全画面共通のNavバー(画面右上)、サイドバーやコンテンツエリア(機能ページ)を作成します。

![template](https://i.gyazo.com/4ce6468143c9740a2ca87566557de494.png)

サイトバー、Navバーについては、案件に合わせて必要なメニューへのリンクを記述する。  
fontsomeaweを使用すると、キレイなアイコンをクラス指定だけで使うことができるのでおすすめ  
CDNは上記で指定しているので、下記を参考に、このみのアイコンを使用する。  
https://fontawesome.com/icons?d=gallery&p=2  



### 課題3:ルーティングの作成
以下を参考にして、app/urls.pyや各アプリのurlsを作成して、ルーティングを定義してください。  
最終的には、作成したページ全てのルーティングを行う必要がありますが、  
ここでは、以下のルートのurls.pyの作成と、settingアプリのurls.pyを作成してください。  
以下で示しているsetting/urls.pyに対して、今回使用するsampleページへのルーティングを追記してください。

今回は、アプリは4つ作る想定なので、以下のようにする  
app/urls.py
```
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # 管理画面（案件ではセキュリティ上、PATHを既知のadmin以外にする方が良い）
    path('', include('django.contrib.auth.urls')), #  ログイン系処理に必要なので追加
    path('syuppin/', include("syuppin.urls")),
    path('setting/', include("setting.urls")),
    path('mypage/', include("mypage.urls")),
    path('users/', include("users.urls"))
]
```

各アプリには既定ではurls.pyが存在しないので、app/urlsをコピーするなどして作成する。  
一例として、settingsのurls.pyの例で説明する。  
setting/urls.py  
```
# 必要な各Viewファイルを全てインポートする
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

app_name = 'setting' # この名前でアクセスできるようになる 例：{% url 'setting:asin' %}
urlpatterns = [
    # pathはurlに表示されるPATH、Viewクラス、templateからアクセスするための名前の順で指定する
    path('replace-word', ReplaceWordView.as_view(), name="replace-word"),
    path('common-setting',SyuppinCommonSettingView.as_view(), name="common-setting"),
    path('search-word',SearchWordView.as_view(), name="search-word"),
    path('search-word-rakuma',SearchWordView.as_view(), name="search-word-rakuma"),
    path('blacklist-word',BlacklistWordView.as_view(), name="blacklist-word"),
    path('blacklist-seller',BlacklistSellerView.as_view(), name="blacklist-seller"),
    path('fetch-url',FetchUrlView.as_view(), name="fetch-url"),
    path('profit', ProfitView.as_view(), name="profit"),
]
```

### 課題4:Formからのデータ登録、編集（CRUD）
本案件においては、応用的なフォームしか使用しておらず、はじめの学習には不向きなため  
別案件で使用した基礎的かつ一般的なフォームによるCRUDの練習を行います。  
（最終的なWebサイトでは使わないページだが練習用として作成する）

以下のファイルに完成形が記載してありますので適宜参照してください。
```
views/sample_form.py
forms/sample_form.py
models/saple_form.py
tamplates/setting/sample.html
```

### フォルダ構造について
Django既定では、ModelやViewは、models.pyやviews.pyといった１つのファイルを  
１アプリにつき１ファイルずつ用意するようになっていますが  
規模が大きくなると管理するのが困難になります。  
そこで本案件では、modelsやviewsといったフォルダを作成し  
そこに、sample.pyなどの各ファイルを格納していく方式を採用しています。  

そのため、既定のmodels.py等のファイルは削除して、代りにmodelsフォルダを  
アプリ内に作成します。

#### 実装したい要件
フォーム画面からDBに情報を登録、変更、表示を行いたい。  
フォームの項目はinput入力の他、選択肢、複数行のinputを可能としたい。  
完成形では実際の案件のため、カラム項目数がかなり多いため  
練習が目的であれば、いくつか選択して実装する形でも構いません。  

#### Task
上記の要件に対してフォーム画面を実装してください。  
1. settingアプリにmodels、forms、viewsフォルダを作成してください。  
2. sample_formモデルを作成してMigrateしてください(カラムの項目は完成品を参照)  
※なお、選択肢の項目はchoicesにで指定します。   
参考:https://qiita.com/ryu22e/items/37bf4f5f6b60ccccebe2
2. FormをModelFormクラスを使用して作成して先程作成したModelと紐付けてください  
参考:https://noumenon-th.net/programming/2019/11/07/django-modelform/
1. Viewを作成して、GETでフォームが表示できるようにしてください（要urlsへの追加）  
参考:https://django.kurodigi.com/form/
1. Htmlを作成して、GETで返したformのobjectを表示できるようにしてください  
参考:https://qiita.com/frosty/items/e340365684f679b9e5ca
1. Viewを修正して、POSTでフォームの内容を更新できるようにしてください  
参考:https://yuki.world/django-modelform-update-pitfall/

#### 実装例
setting/views/sample_form.py に実装例をアップしています。  
TemplateViewを使用しており、Form、TableやCreate、Updateに関わらず  
汎用的に対応できる実装となっております。  



=====
★★★★★★★★　　以降は作成中。　★★★★★★★★　　

### Tableへのデータ表示、編集、削除(CRUD)
### Excel出力
- openpyxlを使用してテンプレートExcelを読み込む。
- 読み込んだExcelを編集する。
- ExcelをWeb画面から出力(ダウンロード)できるようにする。
### Excelの各カラムとDBデータとの紐付けをテーブルで制御する

## スクレイピング
### SQLAlchemyの定義
### スクレイピングengineの作成
### スクレピング→DBデータ投入
### DBでURLを指定したスクレピング
### DBでキーワードを指定したスクレピング
### DBで除外ワード等を指定したスクレピング結果の除外処理