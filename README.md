
# Blog Marketplace

Блог

## 🚀 Технологии

- FastAPI
- PostgreSQL
- Celery + RabbitMQ
- MinIO (S3-совместимое хранилище)
- Docker + Docker Compose

## 📦 Требования

- Python 3.12
- Docker
- Docker Compose
- Poetry

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/blog-marketplace.git
cd blog-marketplace
```

2. Установите зависимости:
```bash
poetry install
```

3. Создайте файл `.env` на основе `.env.example`

4. Запустите проект:
```bash
docker-compose up -d
```

## 🏗 Архитектура

Проект построен по принципам чистой архитектуры:

- `src/app` - FastAPI приложение
- `src/api` - API эндпоинты
- `src/domain` - бизнес-логика и модели
- `src/application` - сценарии использования
- `src/infrastructure` - внешние сервисы и адаптеры
- `src/schemas` - Pydantic модели
- `src/tasks` - Celery задачи
- `src/middleware` - FastAPI middleware
- `src/auth` - аутентификация и авторизация
- `src/utils` - утилиты
- `src/scripts` - скрипты для инициализации

## 🧪 Тестирование

```bash
# Запуск линтеров
poetry run ruff check src
poetry run mypy src

# Запуск тестов
poetry run pytest
```

## 🔄 CI/CD

Проект использует GitHub Actions для:
- Запуска тестов
- Проверки линтеров
- Тестирования миграций

## 📝 API Документация

После запуска проекта документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐳 Docker

- API: http://localhost:8000
- MinIO Console: http://localhost:9001
- RabbitMQ Management: http://localhost:15672
- PostgreSQL: localhost:5432

## 📄 Лицензия

MIT