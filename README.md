# DRF Online Store

Учебный проект, в котором основной фокус сделан на практическом изучении Django REST Framework (DRF). Архитектура разделена на:
- `main-api` — backend на Django REST Framework
- `frontend` — frontend на Flask
- `db` — PostgreSQL
- `nginx` — reverse proxy

Проект запускается в Docker Compose и поддерживает локальную разработку через `Makefile`.

## Цель проекта

Проект создан как учебный стенд для отработки ключевых подходов DRF на доменной модели интернет-магазина.
В реализации использованы `ModelViewSet` и generic API views, JWT-аутентификация (`simplejwt`), фильтрация/поиск/сортировка и пагинация, API для корзины и заказов, а также автодокументация через Swagger/ReDoc (`drf-yasg`).

## Стек

- Python 3.11+
- Django 5 + DRF
- Flask 3
- PostgreSQL 15
- Docker / Docker Compose
- uv (менеджер зависимостей и запуск команд)
- Ruff (lint/format)
- GitHub Actions (CI)

## Структура проекта

- `main-api/` — Django API (приложения: `products`, `accounts`, `cart`, `order`)
- `frontend/` — Flask-приложение с шаблонами
- `nginx/` — конфиг и Dockerfile для nginx
- `scripts/init-env.sh` — инициализация `.env` из шаблона
- `docker-compose.yaml` — базовый compose
- `docker-compose.dev.yaml` — dev-override (порты, volume, runserver/flask run)
- `Makefile` — основные команды разработки

## Быстрый старт (dev)

### 1) Подготовка окружения

```bash
make env-init
```

Команда создаст `.env` (на основе `.env.example`, если его нет).

### 2) Сборка и запуск

```bash
make build-dev
make run-dev
```

### 3) Применение миграций

```bash
make migrate
```

### 4) (Опционально) Загрузка тестовых данных

```bash
make load-fixtures
```

## Доступные сервисы

После запуска доступны:

- Приложение через nginx: `http://localhost`
- Django API напрямую(dev): `http://localhost:8000`
- Flask frontend напрямую(dev): `http://localhost:5000`
- PostgreSQL(dev): `localhost:5432`

## API и документация

Основные маршруты API:

- Товары и категории:
  - `GET /api/products/`
  - `GET /api/categories/`
- Аккаунты:
  - `POST /api/accounts/register/`
  - `POST /api/accounts/token/`
  - `POST /api/accounts/token/refresh/`
- Корзина:
  - `GET /api/cart/`
  - `POST /api/cart/items/`
  - `DELETE /api/cart/items/<id>/`
- Заказы:
  - `POST /api/order/create/`
  - `GET /api/order/list/`

Swagger / ReDoc:

- `http://localhost:8000/swagger/`
- `http://localhost:8000/redoc/`

## Команды разработки

```bash
make run-dev                 # поднять сервисы
make down-dev                # остановить сервисы
make down-dev ARGS="-v"      # остановить и удалить volume

make logs-dev SERVICE="main-api"
make shell-service-dev SERVICE="main-api"

make migrate
make load-fixtures

make lint
make lint-fix
make fmt
make format-check
make test
make check
```

## Тесты и качество кода

- Проверка линтинга:
  ```bash
  make lint
  ```
- Проверка форматирования:
  ```bash
  make format-check
  ```
- Запуск тестов:
  ```bash
  make test
  ```

## CI

В `.github/workflows/ci.yml` настроены:
- проверка merge-конфликтов для PR
- lint + format-check + test
- сборка Docker-образов `main-api`, `frontend`, `nginx`

## Остановка и очистка

```bash
make down-dev
make down-dev ARGS="-v"
```

## Примечания

- `frontend` общается с API внутри docker-сети по адресу `http://main-api:8000/api`.
- Для локальной разработки используйте именно связку `docker-compose.yaml + docker-compose.dev.yaml` (это уже зашито в `Makefile`).
