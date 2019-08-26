#!/usr/bin/env bash

cd /var/www/html/django_project
. venv/bin/activate
echo '\e[92m Проверка обновлений списка необходимых модулей:'
pip install -r requirements

cd /var/www/html/django_project/django
echo '\e[92m Сборка статических файлов:'
python manage.py collectstatic --no-input
echo '\e[92m Создание миграций:'
python manage.py makemigrations user core
echo '\e[92m Применение миграций:'
python manage.py migrate

echo '\e[92m Создание индекса на elasticsearch:'
curl -XPUT "elasticsearch:9200/answerly?pretty"

echo '\e[92m Запуск сервера  apache2:'
apache2ctl -D FOREGROUND
