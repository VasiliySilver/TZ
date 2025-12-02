# Техническое задание (TZ)

## Описание задачи

Доделать микросервис, представляющий собой API с двумя эндпоинтами для управления хранилищем книг.

Цель — запустить сервис локально и обеспечить корректную работу эндпоинтов в Swagger.

Предполагается, что таблица "authors" уже заполнена данными. 
Для тестирования допускается вручную добавить авторов в базу данных.


---

## Требования к реализации

1. **Модели**
   - Создать необходимые модели для работы с данными книг и авторов.
   - Обеспечить связь между книгами и авторами.

2. **Миграции**
   - Сгенерировать и применить миграции для создания таблиц в базе данных.

3. **Эндпоинты**
   - Реализовать описанные выше эндпоинты:
     - `POST /api/books` для добавления новой книги.
     - `GET /api/books` для получения списка всех книг.

4. **Тестирование**
   - Убедиться, что эндпоинты корректно отображаются и тестируются в Swagger.

---

###  Для запуска локально:

`docker compose up -d`

`poetry install`

`poetry run python -m src.main`

### Для создания миграций:

`poetry run alembic revision --autogenerate`

`poetry run alembic upgrade head`

---

## Функциональные требования

### API Эндпоинты

1. **Добавление новой книги**
   - **Метод:** `POST`
   - **URL:** `api/books`
   - **Описание:** Позволяет добавить новую книгу в хранилище.
   - **Структура входных данных:**
     ```json
     {
       "title": "The Great Gatsby",
       "authors": [
         "123e4567-e89b-12d3-a456-426614174000"
       ],
       "publication_year": 1925,
       "pages": 180,
       "genre": "Novel"
     }
     ```

2. **Получение списка всех книг**
   - **Метод:** `GET`
   - **URL:** `api/books`
   - **Описание:** Возвращает список всех книг, хранящихся в системе.
   - **Структура ответа:**
     ```json
     [
       {
       "id": "e2fcebf1-dfe5-4ddd-9cef-5c25c76afca8",
       "title": "The Great Gatsby",
       "authors": [
         "123e4567-e89b-12d3-a456-426614174000"
       ],
       "publication_year": 1925,
       "pages": 180,
       "genre": "Novel"
     }
     ]
     ```

# Book Management API

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)](https://www.postgresql.org/)
[![Test Coverage](https://img.shields.io/badge/coverage-88%25-brightgreen.svg)]()

Микросервис для управления книгами, построенный на принципах **Clean Architecture**, **Domain-Driven Design (DDD)**, **CQRS** и **Event-Driven Architecture**.

## 🎯 Описание

RESTful API для управления библиотекой книг и авторов с асинхронной обработкой событий через RabbitMQ.

### Основные возможности

- ✅ CRUD операции для книг и авторов
- ✅ Валидация бизнес-правил (количество страниц > 0, минимум 1 автор)
- ✅ Асинхронная обработка событий (создание, обновление, удаление)
- ✅ Интеграция с RabbitMQ для event-driven архитектуры
- ✅ PostgreSQL для хранения данных
- ✅ Comprehensive test coverage (88%)
- ✅ Docker и Kubernetes deployment
- ✅ Swagger UI для тестирования API

## 🏗️ Архитектура

Проект реализует **Clean Architecture** с чёткым разделением слоёв:

```
src/
├── domain/          # Бизнес-логика, entities, repository interfaces
├── application/     # Use cases, commands, queries, handlers
├── infrastructure/  # Реализация репозиториев, БД, messaging
└── presentation/    # API endpoints, schemas, dependency injection
```

### Паттерны

- **Domain-Driven Design (DDD)**: Entities, Value Objects, Domain Events
- **CQRS**: Разделение Command и Query
- **Repository Pattern**: Абстракция работы с данными
- **Unit of Work**: Управление транзакциями
- **Event-Driven Architecture**: Асинхронная обработка через RabbitMQ
- **Dependency Injection**: Чистые зависимости между слоями

## 🚀 Quick Start

### Использование Makefile (рекомендуется)

```bash
# Показать все доступные команды
make help

# Установить зависимости
make install

# Запустить локальную инфраструктуру (PostgreSQL + RabbitMQ)
make docker-local

# Применить миграции
make migrate

# Заполнить БД тестовыми данными
make seed

# Запустить API
make run

# Запустить consumer (в другом терминале)
make consumer
```

API будет доступен по адресу: http://localhost:8000

Swagger UI: http://localhost:8000/docs

### Ручной запуск (без Makefile)

```bash
# Установка зависимостей
poetry install

# Запуск инфраструктуры
cd deployment/local && docker compose up -d

# Миграции
poetry run alembic upgrade head

# Seed данных
poetry run python scripts/seed_data.py

# Запуск API
poetry run python -m src.main

# Запуск consumer (отдельный терминал)
poetry run python scripts/run_consumer.py
```

## 📋 Makefile Commands

### Development

```bash
make install          # Установить зависимости
make run             # Запустить API server
make dev             # Запустить с hot-reload
make consumer        # Запустить event consumer
```

### Database

```bash
make migrate                    # Применить миграции
make migrate-create msg="..."   # Создать новую миграцию
make migrate-down               # Откатить последнюю миграцию
make seed                       # Заполнить тестовыми данными
make db-reset                   # Сбросить БД (все таблицы)
```

### Testing

```bash
make test            # Запустить все тесты
make test-unit       # Только unit-тесты
make test-integration # Только integration-тесты
make coverage        # Тесты с coverage report
make coverage-report # Открыть HTML отчёт
```

### Code Quality

```bash
make lint            # Проверить код (ruff)
make lint-fix        # Исправить проблемы автоматически
make format          # Отформатировать код
make format-check    # Проверить форматирование
make check           # Запустить все проверки (lint + format + test)
```

### Docker - Local (только инфраструктура)

```bash
make docker-local       # Запустить PostgreSQL + RabbitMQ
make docker-local-down  # Остановить
make docker-local-logs  # Показать логи
```

### Docker - Dev (полный стек)

```bash
make docker-dev         # Запустить все сервисы
make docker-dev-build   # Собрать и запустить
make docker-dev-down    # Остановить
make docker-dev-logs    # Показать логи
make docker-dev-restart # Перезапустить
```

### Docker - Prod

```bash
make docker-prod       # Запустить prod окружение
make docker-prod-build # Собрать и запустить
make docker-prod-down  # Остановить
make docker-prod-logs  # Показать логи
```

### Docker - Утилиты

```bash
make docker-ps       # Показать запущенные контейнеры
make docker-clean    # Удалить все контейнеры, образы, volumes
make docker-rebuild  # Пересобрать образы без кэша
```

### Kubernetes

```bash
make k8s-local    # Deploy в minikube
make k8s-prod     # Deploy в prod
make k8s-delete   # Удалить ресурсы
make k8s-status   # Статус pods
make k8s-logs     # Логи API pod
```

### Утилиты

```bash
make clean        # Очистить __pycache__, .pytest_cache и т.д.
make ci           # Полный CI pipeline (clean + install + lint + test + coverage)
```

## 🔌 API Endpoints

### Books

```http
POST   /api/v1/books/      # Создать книгу
GET    /api/v1/books/      # Получить все книги
GET    /api/v1/books/{id}  # Получить книгу по ID
PUT    /api/v1/books/{id}  # Обновить книгу
DELETE /api/v1/books/{id}  # Удалить книгу
```

### Authors

```http
GET    /api/v1/authors/    # Получить всех авторов
```

### Пример запроса

```bash
# Создать книгу
curl -X POST "http://localhost:8000/api/v1/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "authors": ["123e4567-e89b-12d3-a456-426614174000"],
    "publication_year": 1925,
    "pages": 180,
    "genre": "Novel"
  }'

# Или через Makefile + httpx
make run  # в одном терминале
```

## 🧪 Testing

```bash
# Все тесты
make test

# С coverage
make coverage

# Только unit-тесты (быстрые, с моками)
make test-unit

# Только integration-тесты (с реальной БД)
make test-integration

# Открыть HTML отчёт
make coverage-report
```

### Test Coverage: 88%

- ✅ Unit tests для репозиториев
- ✅ Unit tests для command handlers
- ✅ Integration tests для API endpoints
- ✅ Моки для EventPublisher (без RabbitMQ в тестах)

## 🐳 Docker Deployment

Проект поддерживает несколько окружений:

### 1. Local (только инфраструктура)

Для разработки - запускает только PostgreSQL и RabbitMQ, API запускается локально.

```bash
make docker-local
make migrate
make run
```

### 2. Dev (полный стек)

Все сервисы в Docker с hot-reload и debug режимом.

```bash
make docker-dev-build
make docker-dev-logs
```

Доступ:
- API: http://localhost:8000
- RabbitMQ UI: http://localhost:15672 (guest/guest)

### 3. Prod (production-ready)

С ресурс-лимитами, healthchecks, restart policies.

```bash
make docker-prod-build
```

## ☸️ Kubernetes (TODO)

```bash
# Запустить minikube
minikube start

# Deploy в локальный кластер
make k8s-local

# Проверить статус
make k8s-status

# Открыть API через minikube
minikube service tz-api

# Удалить
make k8s-delete
```

## 🛠️ Tech Stack

- **Python 3.12** - Programming language
- **FastAPI** - Web framework
- **SQLAlchemy 2.0** - ORM (async)
- **PostgreSQL 17** - Database
- **RabbitMQ 3** - Message broker
- **Alembic** - Database migrations
- **Pydantic 2.0** - Data validation
- **pytest** - Testing framework
- **Docker** - Containerization
- **Poetry** - Dependency management

## 📁 Project Structure

```
.
├── src/
│   ├── domain/                    # Domain layer
│   │   ├── entities/              # Business entities
│   │   ├── repositories/          # Repository interfaces
│   │   └── events/                # Domain events
│   ├── application/               # Application layer
│   │   ├── commands/              # Command handlers
│   │   ├── queries/               # Query handlers
│   │   └── services/              # Application services
│   ├── infrastructure/            # Infrastructure layer
│   │   ├── database/              # Database models & repos
│   │   └── messaging/             # RabbitMQ integration
│   ├── presentation/              # Presentation layer
│   │   └── api/                   # REST API endpoints
│   ├── tests/                     # Test suite
│   │   ├── unit/                  # Unit tests
│   │   └── integration/           # Integration tests
│   ├── app_config.py              # Configuration
│   └── main.py                    # Application entry point
├── deployment/                    # Deployment configs
│   ├── docker/                    # Dockerfiles
│   ├── local/                     # Local dev compose
│   ├── dev/                       # Dev environment compose
│   ├── prod/                      # Prod environment compose
│   └── kubernetes/                # K8s manifests (TODO)
├── scripts/                       # Utility scripts
│   ├── seed_data.py              # Database seeding
│   ├── run_consumer.py           # Event consumer
│   └── entrypoint.sh             # Docker entrypoint
├── pyproject.toml                # Poetry config
├── alembic.ini                   # Alembic config
├── Makefile                      # Development commands
└── README.md                     # This file
```

## 🔧 Configuration

Настройки через environment variables:

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

## 🎓 Learning Outcomes

Этот проект демонстрирует:

- ✅ Clean Architecture implementation
- ✅ Domain-Driven Design patterns
- ✅ CQRS with Commands and Queries
- ✅ Event-Driven Architecture with RabbitMQ
- ✅ Repository Pattern with Unit of Work
- ✅ Dependency Injection
- ✅ Test-Driven Development (TDD)
- ✅ Comprehensive testing (unit + integration)
- ✅ Docker multi-stage builds
- ✅ Multi-environment deployment strategy
- ✅ Makefile for developer experience

## 📝 License

MIT

## 👤 Author

VasiliySilver - [GitHub](https://github.com/VasiliySilver/TZ)
