"""
Настройка базы данных и сессий
Базовые модели с общими полями
Инициализация и проверка подключения
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, String, func, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.sqltypes import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from loguru import logger
import uuid
import asyncio

from core.settings import settings

# Создание движка БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # SQL логи в debug режиме
    future=True,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,   # Пересоздание соединений каждый час
)

# Фабрика сессий
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Базовый класс для моделей
Base = declarative_base()


class GUID(TypeDecorator):
    """Тип данных для UUID"""
    impl = CHAR
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value)).replace('-', '')
            else:
                return str(value).replace('-', '')
    
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value


class BaseModel(Base):
    """
    Базовая модель с общими полями
    Все модели должны наследоваться от неё
    """
    __abstract__ = True
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Для soft delete
    
    def soft_delete(self):
        """Мягкое удаление записи"""
        self.deleted_at = datetime.utcnow()
    
    @property
    def is_deleted(self) -> bool:
        """Проверка удалена ли запись"""
        return self.deleted_at is not None


async def check_database_connection() -> bool:
    """Проверка подключения к базе данных"""
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✓ Подключение к БД успешно")
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка подключения к БД: {e}")
        logger.error(f"URL подключения: {settings.DATABASE_URL.replace(settings.DB_PASSWORD, '***')}")
        return False


async def create_tables():
    """Создание всех таблиц"""
    try:
        logger.info("Создание таблиц БД...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✓ Таблицы БД созданы успешно")
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка создания таблиц: {e}")
        return False


async def drop_tables():
    """Удаление всех таблиц"""
    try:
        logger.info("Удаление таблиц БД...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("✓ Таблицы БД удалены успешно")
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка удаления таблиц: {e}")
        return False


async def init_database():
    """
    Инициализация базы данных
    Проверка подключения и создание таблиц
    """
    logger.info("Инициализация базы данных...")
    
    # Проверяем подключение
    if not await check_database_connection():
        logger.error("Не удалось подключиться к БД. Проверьте настройки.")
        return False
    
    # Создаем таблицы
    if not await create_tables():
        logger.error("Не удалось создать таблицы БД.")
        return False
    
    logger.info("✓ База данных инициализирована успешно")
    return True


async def close_database():
    """Закрытие соединений с БД"""
    try:
        await engine.dispose()
        logger.info("✓ Соединения с БД закрыты")
    except Exception as e:
        logger.error(f"✗ Ошибка закрытия соединений с БД: {e}")
