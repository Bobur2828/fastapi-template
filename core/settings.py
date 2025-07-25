from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    """Настройки приложения"""

    # Основные настройки
    APP_NAME: str = "FastAPI App"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Выбор СУБД
    DB_USE_PGSQL: bool = False  # True - PostgreSQL, False - SQLite

    # Настройки PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # Настройки SQLite
    SQLITE_DB_PATH: str = "sqlite3.db"  # Путь к файлу базы

    # Безопасность
    BEARER_TOKEN: str = "change-me-in-production"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Логирование
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Формируем DATABASE_URL в зависимости от СУБД"""
        if self.DB_USE_PGSQL:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"

    class Config:
        env_file = ".env"
        env_prefix = "APP_"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
