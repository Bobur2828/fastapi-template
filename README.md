# FastAPI Project

Проект создан с помощью FastAPI Template Generator.

## Структура проекта

```
app/
├── app.py                 # Точка входа приложения
├── core/                  # Ядро приложения
│   ├── settings.py       # Настройки через pydantic-settings
│   ├── db.py            # Конфигурация базы данных
│   ├── logger.py        # Настройка логирования
│   └── dependencies.py  # Общие зависимости
├── middleware/           # Middleware компоненты
│   ├── error_handler.py # Обработка ошибок
│   ├── logging.py       # Логирование запросов
│   └── cors.py          # CORS настройки
├── shared/              # Общие компоненты
│   ├── schemas/         # Базовые схемы
│   └── models/          # Базовые модели
├── modules/             # Бизнес модули
│   └── echo/           # Пример модуля
├── utils/               # Утилиты
└── logs/                # Логи
```

## Установка и запуск

### Локально

```bash
# Установка зависимостей
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Настройка окружения
cp .env.example .env
# Отредактировать .env файл

# Запуск
uvicorn app:app --reload
```

### Docker

```bash
# Запуск с базой данных
docker-compose up -d

# Только приложение
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

## Использование

### API Документация

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Health Check

- Health endpoint: http://localhost:8000/health

### Примеры запросов

```bash
# Публичный эндпоинт
curl -X POST http://localhost:8000/api/echo/ \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello World"}'

# Защищенный эндпоинт (требует Bearer токен)
curl -X POST http://localhost:8000/api/echo/protected \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-bearer-token" \
     -d '{"message": "Protected Hello"}'
```

## Разработка

### Форматирование кода

```bash
make format  # Автоформатирование
make lint    # Проверка стиля
```

### Создание нового модуля

1. Создайте папку в `modules/`
2. Добавьте файлы: `router.py`, `schemas.py`, `services.py`, `models.py`
3. Подключите роутер в `app.py`

### Работа с базой данных

```bash
# Создать новую миграцию
make db-revision MSG="Описание изменений"

# Применить миграции
make db-upgrade

# Откатить миграции
make db-downgrade
```

## Настройки

Все настройки в файле `.env`:

- `APP_DATABASE_URL` - строка подключения к БД
- `APP_BEARER_TOKEN` - токен для защищенных эндпоинтов
- `APP_DEBUG` - режим отладки
- `APP_ALLOWED_ORIGINS` - разрешенные origins для CORS

## Логирование

Логи пишутся в:
- Консоль (для разработки)
- `logs/app.log` (все логи)
- `logs/app_errors.log` (только ошибки)

## Особенности

### Модульная архитектура

Каждый модуль содержит:
- `router.py` - API эндпоинты
- `schemas.py` - Pydantic модели
- `services.py` - бизнес-логика
- `models.py` - ORM модели
- `funcs.py` - вспомогательные функции

### Стандартные ответы

Все ответы в формате:
```json
{
  "status": "ok",
  "data": {...},
  "message": "Optional message"
}
```

### Базовые модели

Все модели БД наследуются от `BaseModel` и содержат:
- `id` (UUID)
- `created_at` 
- `updated_at`
- `deleted_at` (для soft delete)

### Middleware

- Обработка ошибок
- Логирование запросов
- CORS настройки
- Добавление заголовков ответа

## Безопасность

- Bearer токен для защищенных эндпоинтов
- Валидация всех входных данных
- CORS настройки
- Логирование подозрительной активности

## Производительность

- Async/await для всех операций
- Connection pooling для БД
- Оптимизированные запросы с пагинацией
- Кеширование (при необходимости)

## Мониторинг

- Health check эндпоинт
- Подробные логи
- Метрики времени обработки запросов
- Отслеживание ошибок
