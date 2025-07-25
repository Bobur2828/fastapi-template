"""
FastAPI ilovasi
Kirish nuqtasi, middleware sozlamalari va marshrutlarni ulash
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from core.settings import settings
from core.logger import setup_logging
from core.db import init_database, close_database
from middleware.error_handler import error_handler_middleware
from middleware.logging import logging_middleware
from modules.echo.router import router as echo_router

# Loglashni sozlash
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ilovaning hayotiy tsiklini boshqarish"""
    # Ishga tushirish
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} ishga tushdi")
    
    # Ma'lumotlar bazasini ishga tayyorlash
    if not await init_database():
        logger.error("❌ Ma'lumotlar bazasini ishga tushirib bo‘lmadi. Ilova to‘xtatildi.")
        raise RuntimeError("Ma'lumotlar bazasi ishga tushmadi")
    
    logger.info("✅ Ilova ishga tayyor")
    
    yield
    
    # To‘xtatish
    logger.info("🛑 Ilova to‘xtatilmoqda...")
    await close_database()
    logger.info("👋 Ilova muvaffaqiyatli to‘xtatildi")


# Ilovani yaratish
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Modulli arxitekturaga ega FastAPI ilovasi",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Middleware'lar (tartib muhim!)
app.middleware("http")(error_handler_middleware)
app.middleware("http")(logging_middleware)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlarni ulash
app.include_router(echo_router, prefix="/api/echo", tags=["echo"])


@app.get("/health")
async def health_check():
    """Xizmat va ma'lumotlar bazasi holatini tekshirish"""
    from core.db import check_database_connection
    
    db_status = await check_database_connection()
    
    return {
        "status": "ok" if db_status else "warning",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "ulandi" if db_status else "ulanmadi"
    }


@app.get("/")
async def root():
    """Ilovaning asosiy endpointi"""
    return {
        "message": f"{settings.APP_NAME} ilovasiga xush kelibsiz!",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Ishlab chiqarish rejimida hujjatlar o‘chirib qo‘yilgan",
        "health": "/health"
    }
