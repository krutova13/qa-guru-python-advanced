# FastAPI Project

Проект на FastAPI с использованием SQLModel для работы с базой данных PostgreSQL.

## Требования

- Python 3.13+
- PostgreSQL
- Poetry (для управления зависимостями)
- Docker и Docker Compose (для запуска в контейнерах)

## Установка и запуск

### Вариант 1: Локальная установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd fastApiProject
```

2. Установите зависимости:
```bash
poetry install
```

3. Создайте файл `.env` в корневой директории проекта:
```env
APP_URL=
DATABASE_ENGINE=
DATABASE_POOL_SIZE=
STORAGE_TYPE=
HOST=localhost
PORT=8000
```

4. Запустите сервер:
```bash
poetry run python app/main.py
```

### Вариант 2: Запуск в Docker

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd fastApiProject
```

2. Создайте файл `.env` в корневой директории проекта:
```env
APP_URL=
DATABASE_URL=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

3. Запустите приложение с помощью Docker Compose:
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

## Структура Docker

Проект использует два контейнера:
- `app` - FastAPI приложение
- `db` - PostgreSQL база данных

Контейнеры связаны между собой через Docker network, что обеспечивает:
- Изоляцию окружения
- Простоту развертывания
- Масштабируемость
- Управление зависимостями

## API Endpoints

### Пользователи

- `GET /api/v1/users` - Получить список пользователей
- `POST /api/v1/users` - Создать пользователя
- `GET /api/v1/users/{user_id}` - Получить пользователя по ID
- `PATCH /api/v1/users/{user_id}` - Обновить пользователя
- `DELETE /api/v1/users/{user_id}` - Удалить пользователя
- `GET /api/v1/users/{user_id}/products` - Получить продукты пользователя
- `GET /api/v1/users/{user_id}/products/{product_id}` - Получить конкретный продукт пользователя

### Продукты

- `GET /api/v1/products` - Получить список продуктов
- `POST /api/v1/products` - Создать продукт
- `GET /api/v1/products/{product_id}` - Получить продукт по ID
- `DELETE /api/v1/products/{product_id}` - Удалить продукт

## Тестирование

### Локальное тестирование
```bash
poetry run pytest
```

### Тестирование в Docker
```bash
docker-compose run app pytest
```

## Особенности проекта

1. Использование SQLModel для работы с базой данных
2. Пагинация для списков пользователей и продуктов
3. Валидация данных с помощью Pydantic
4. Обработка ошибок и исключений
5. Тесты с использованием pytest
6. Документация API (доступна по адресу http://localhost:8000/docs)
7. Контейнеризация с помощью Docker
8. Автоматическое создание и настройка базы данных при запуске
