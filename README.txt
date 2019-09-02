Данный репозиторий посвящен проекту Answerly, который представляет из себя сайт, где пользователи могут задавать интересующие их вопросы и отвечать на них. В качестве дополнительной функциональности добавлено взаимодействие с Elasticsearch, а также реализовано использование API Mailer (http://li2042-77.members.linode.com/, https://github.com/TigenTigen/mailer) для обеспечения оповещения пользователей о новых ответах на интересующие их вопросы.

Для развертки проекта создаются четыре docker-контейнера:
postgres - PostgreSQL-сервер для размещения базы данных сайта.
elasticsearch - Elasticsearch-сервер, для обеспечения поиска по сайту.
apache - основной контейнер, в котором размещается код проекта на языке python, и apache-сервер для его "распространения". Исходный код для сборки изображения располагается в директории /apache.
nginx - nginx-сервер, работающий по принципу прокси-сервера, а также обеспечивающий обработку статических данных сайта. Исходный код для сборки изображения располагается в директории /nginx.

Для указания конфиденциальной информации, необходимой для работы проекта используются docker-secrets, расположенные в папке secrets:
      - psql-pw - пароль базы данных,
      - psql-user - имя пользователя базы данных,
      - psql-db - имя базы данных проекта,
      - django-sk - "секретный ключ" проекта (настройка SECRET_KEY),
      - django-ehu - электронный адрес почты gmail, используемый для отправки писем,
      - django-ehp - пароль от аккаунта gmail,
      - es-un - имя пользователя для Elasticsearch-сервера,
      - es-pw - пароль Elasticsearch-сервера,
      - mailer-un - имя пользователя для авторизации в Mailer,
      - mailer-pw - пароль от аккаунта на сайте Mailer.
В данном репозитории все файлы в папке secrets пусты, при запуске проекта в них необходимо записать собственные значения.

Запуск контейнеров:
Версия для локальной работы системы может быть запущена посредством сценария run_local.sh.
Версия для постоянной работы сервера:
docker stack deploy -c docker-compose.yml ANSWERLY
При запуске должны быть определены переменые среды:
HOST_IP - IP адрес сервера, на котором запускается проект (напр. 127.0.0.1),
HOST_NAME - имя сервера, на котором запускается проект (напр. localhost).

Подготовка сервера для развертки:

1. Обновление системы:
apt-get update && apt-get upgrade

2. Установка и настройка git:
apt-get install git
export git_user_name='...'                # введите собственное значение
export git_user_email='...'               # введите собственное значение
git config --global user.email $git_user_email && git config --global user.name $git_user_name

3. Установка docker (для ubuntu):
apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io

4. Установка docker-compose (для ubuntu):
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

5. Задание переменных окружения:
export HOST_IP='...'                # введите собственное значение
export HOST_NAME='...'               # введите собственное значение
