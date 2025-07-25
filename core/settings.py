from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    """Ilova sozlamalari"""

    # Asosiy sozlamalar
    APP_NAME: str = "FastAPI Ilovasi"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Ma'lumotlar bazasi turi
    DB_USE_PGSQL: bool = False  # True - PostgreSQL, False - SQLite

    # PostgreSQL sozlamalari
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # SQLite sozlamalari
    SQLITE_DB_PATH: str = "sqlite3.db"  # Baza faylining yo‘li

    # Xavfsizlik
    BEARER_TOKEN: str = "ishlab-chiqarishda-almashtiring"

    # CORS (ruxsat etilgan manbalar)
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Loglash
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Ma'lumotlar bazasi URL manzilini tanlangan turga qarab hosil qilamiz"""
        if self.DB_USE_PGSQL:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"

    class Config:
        env_file = ".env"               # Muhit o‘zgaruvchilari fayli
        env_prefix = "APP_"            # Har bir o‘zgaruvchi uchun prefiks
        case_sensitive = False         # Katta-kichik harf farqlanmaydi


# Sozlamalarning global nusxasi
settings = Settings()
