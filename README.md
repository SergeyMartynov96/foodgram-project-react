# Проект Продуктовый помощник - Foodgram
### Описание проекта:

Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления выбранных блюд.
 
Вот, что было сделано в ходе работы над проектом:
- настроено взаимодействие Python-приложения с внешними API-сервисами;
- создан собственный API-сервис на базе проекта Django;
- подключено SPA к бэкенду на Django через API;
- созданы образы и запущены контейнеры Docker;
- созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения;
- закреплены на практике основы DevOps, включая CI&CD.

## Технологии

- Python 3.9
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Gunicorn
- Nginx
- Github Actions

### Как запустить проект локально в контейнерах:

Клонировать репозиторий и перейти в него в командной строке:

``` git@github.com:SergeyMartynov96/foodgram-project-react.git ``` 
``` cd foodgram-project-react ``` 

Запустить docker-compose:

```
docker-compose up

```

После окончания сборки контейнеров выполнить миграции:

```
docker-compose exec web python manage.py migrate

```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser

```

Загрузить статику:

```
docker-compose exec web python manage.py collectstatic --no-input 

```

Проверить работу проекта по ссылке:

```
http://localhost/
```

### Над бэкендом проекта работал
- [Сергей Мартынов](https://github.com/SergeyMartynov96)

Фронтенд:
- [@practicum-russia](https://github.com/yandex-praktikum)