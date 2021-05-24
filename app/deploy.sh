#! bin/sh
git pull
cp .env.prod .env
pkill gunicorn
. venv/bin/activate
gunicorn --bind 127.0.0.1:8000 app.wsgi -D