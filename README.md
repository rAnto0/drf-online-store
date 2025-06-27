# Запуск проекта

1. Создать в корне проекта **.env** с содержимым:
```
DEBUG=True
DB_NAME=dbname
DB_USER=dbusername
DB_PASSWORD=dbpass
DB_HOST=db
DB_PORT=5432
SECRET_KEY_MAIN_API=djangosecretkey
DJANGO_ALLOWED_HOSTS=main-api,localhost,127.0.0.1

DJANGO_SETTINGS_MODULE=zaharovo.settings
```

2. Запуск с помощью **docker-compose**

2.1. Сборка, запуск и остановка
    Собрать и запустить
    ```bash
    docker compose up --build
    ```

    Остановить
    ```bash
    docker compose down
    ```

2.2. Выполнение миграций и загрузка fixtures
    Запуск консоли сервиса main-api*(ctrl+D выйти)*
    ```bash
    docker compose exec main-api bash
    ```

    Выполнение миграций
    ```bash
    python manage.py migrate
    ```

    Загрузка шаблона
    ```bash
    python manage.py loaddata generated_products.json
    ```

2.3. Заходим на сайт
    http://127.0.0.1:5000/ - фронтенд
    http://localhost:8000/ - api
