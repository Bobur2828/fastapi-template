# Makefile для удобной работы с проектом

.PHONY: help install run dev test lint format clean docker-up docker-down

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt

run: ## Запустить сервер
	uvicorn app:app --host 0.0.0.0 --port 8000

dev: ## Запустить в режиме разработки
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

test: ## Запустить тесты
	pytest

lint: ## Проверить код линтерами
	flake8 .
	black --check .
	isort --check .

format: ## Автоформатирование кода  
	black .
	isort .

clean: ## Очистить временные файлы
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

docker-up: ## Запустить через Docker Compose
	docker-compose up -d

docker-down: ## Остановить Docker Compose
	docker-compose down

docker-logs: ## Посмотреть логи Docker
	docker-compose logs -f

docker-build: ## Пересобрать Docker образы
	docker-compose build

# Команды для работы с БД
db-check: ## Проверить подключение к БД
	python -c "import asyncio; from core.db import check_database_connection; asyncio.run(check_database_connection())"

db-init: ## Инициализировать БД (создать таблицы)
	python -c "import asyncio; from core.db import init_database; asyncio.run(init_database())"

db-reset: ## Пересоздать все таблицы (ОСТОРОЖНО!)
	python -c "import asyncio; from core.db import drop_tables, create_tables; asyncio.run(drop_tables()); asyncio.run(create_tables())"

db-url: ## Показать URL подключения к БД
	python -c "from core.settings import settings; print(settings.DATABASE_URL.replace(settings.DB_PASSWORD, '***'))"
