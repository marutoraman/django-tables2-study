### Dockerfileには、Dockerイメージ作成時に行う処理を記述する
### イメージ作成時のため他のコンテナに依存するような処理は行わない

# ベースイメージ
FROM python:3.8.6-alpine3.12

# 環境変数
ENV LANG C.UTF-8
ENV TZ UTC
ENV PYTHONUNBUFFERED 1

# 各種パッケージのインストール
RUN apk add --update bash git curl build-base mariadb-connector-c-dev
RUN apk add mariadb-client

# INSTALL
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . .
#COPY .env.production /home/.env
RUN mkdir -p /var/run/gunicorn

# staticフォルダの作成
RUN mkdir -p /usr/share/nginx/html/static \
 && mkdir -p /usr/share/nginx/html/media \
 && chown -R root /usr/share/nginx/html/static \
 && chown -R root /usr/share/nginx/html/media
