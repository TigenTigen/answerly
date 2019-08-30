#!/usr/bin/env bash

# Задержка необходима, чтобы полностью загрузились контейнеры postgres и elasticsearch
sleep 40

echo '\e[92m Elasticsearch configuration:'
cd /var/www/html/django_project
export ES_USERNAME=$(cat $ES_USERNAME_FILE)
export ES_PASSWORD=$(cat $ES_PASSWORD_FILE)
echo '\e[92m Создание нового пользователя:'
curl -X POST "http://elastic:changeme@elasticsearch:9200/_xpack/security/user/$ES_USERNAME?pretty" -H 'Content-Type: application/json' -d "{\"password\":\"$ES_PASSWORD\", \"roles\": [\"superuser\"]}"
echo '\e[92m Аутентификация нового пользователя и получение информации о состоянии системы:'
curl -u $ES_USERNAME:$ES_PASSWORD http://elasticsearch:9200/_cluster/health?pretty
echo '\e[92m Отключение встроенного пользователя:'
curl -X PUT "http://$ES_USERNAME:$ES_PASSWORD@elasticsearch:9200/_xpack/security/user/elastic/_disable?pretty"
echo '\e[92m Создание индекса answerly:'
curl -XPUT "http://$ES_USERNAME:$ES_PASSWORD@elasticsearch:9200/answery?pretty"

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
echo '\e[92m Обновление поискового индекса:'
python manage.py rebuild_index --noinput

echo '\e[92m Запуск сервера  apache2:'
apache2ctl -D FOREGROUND
