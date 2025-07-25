"""
Ma'lumotlar bazasi va sessiyalarni sozlash
Umumiy ustunlarga ega asosiy modellar
Bazani ishga tushirish va ulanishni tekshirish
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

# Ma'lumotlar bazasi dvigatelini yaratish
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # DEBUG rejimida SQL so‘rovlarini chiqarish
    future=True,
    pool_pre_ping=True,   # Ulanishdan oldin tekshiruv
    pool_recycle=3600,    # Har bir soatdan keyin ulanishni yangilash
)

# Sessiya fabrikasi
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Modellar uchun asosiy klass
Base = declarative_base()


class GUID(TypeDecorator):
    """UUID uchun maxsus ma'lumotlar turi"""
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
    Umumiy ustunlarga ega asosiy model
    Barcha modellar ushbu klassdan meros olishi kerak
    """
    __abstract__ = True

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete uchun

    def soft_delete(self):
        """Yumshoq o‘chirish funksiyasi"""
        self.deleted_at = datetime.utcnow()

    @property
    def is_deleted(self) -> bool:
        """Yozuv o‘chirilganligini tekshirish"""
        return self.deleted_at is not None



async def check_database_connection() -> bool:
    """Ma'lumotlar bazasiga ulanishni tekshirish"""
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✓ Ma'lumotlar bazasiga muvaffaqiyatli ulandi")
        return True
    except Exception as e:
        logger.error(f"✗ Ma'lumotlar bazasiga ulanishda xatolik: {e}")
        logger.error(f"Ulanish manzili (parol yashirilgan): {settings.DATABASE_URL.replace(settings.DB_PASSWORD, '***')}")
        return False


async def create_tables():
    """Barcha jadvallarni yaratish"""
    try:
        logger.info("Ma'lumotlar bazasi jadvallari yaratilmoqda...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✓ Barcha jadvallar muvaffaqiyatli yaratildi")
        return True
    except Exception as e:
        logger.error(f"✗ Jadvallarni yaratishda xatolik: {e}")
        return False


async def drop_tables():
    """Barcha jadvallarni o‘chirish"""
    try:
        logger.info("Ma'lumotlar bazasi jadvallari o‘chirilyapti...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("✓ Barcha jadvallar muvaffaqiyatli o‘chirildi")
        return True
    except Exception as e:
        logger.error(f"✗ Jadvallarni o‘chirishda xatolik: {e}")
        return False


async def init_database():
    """Ma'lumotlar bazasini boshlang‘ich sozlash va tekshirish"""
    logger.info("Ma'lumotlar bazasini boshlang‘ich sozlash...")

    if not await check_database_connection():
        logger.error("Ma'lumotlar bazasiga ulanish muvaffaqiyatsiz. Sozlamalarni tekshiring.")
        return False

    if not await create_tables():
        logger.error("Ma'lumotlar bazasi jadvallarini yaratib bo‘lmadi.")
        return False

    logger.info("✓ Ma'lumotlar bazasi muvaffaqiyatli sozlandi")
    return True


async def close_database():
    """Ma'lumotlar bazasi bilan bog‘lanishni yopish"""
    try:
        await engine.dispose()
        logger.info("✓ Ma'lumotlar bazasi bilan barcha ulanishlar yopildi")
    except Exception as e:
        logger.error(f"✗ Ma'lumotlar bazasini yopishda xatolik: {e}")