"""
Loglash (log yuritish)ni loguru orqali sozlash
Bir marta shu yerda sozlanadi, keyinchalik logger ni istalgan joyda chaqirish mumkin
"""

import sys
from pathlib import Path
from loguru import logger

from core.settings import settings


def setup_logging():
    """Ilova uchun loglashni sozlash"""
    
    # Standart handlerni olib tashlaymiz
    logger.remove()
    
    # Agar loglar uchun papka mavjud bo‘lmasa — yaratamiz
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Log yozuvi formati
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Konsolga chiqarish
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.DEBUG else settings.LOG_LEVEL,
        colorize=True,
    )
    
    # Umumiy log fayliga yozish
    logger.add(
        settings.LOG_FILE,
        format=log_format,
        rotation="10 MB",        # Har 10 MB dan keyin yangi fayl
        retention="7 days",      # Loglar 7 kun saqlanadi
        compression="zip",       # Eski loglar zip holatda saqlanadi
        level=settings.LOG_LEVEL,
        encoding="utf-8",
    )
    
    # Faqat xatoliklar uchun alohida log fayl
    logger.add(
        settings.LOG_FILE.replace(".log", "_errors.log"),
        format=log_format,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
    )
    
    logger.info(f"Loglash sozlandi. Debug rejimi: {settings.DEBUG}, Daraja: {settings.LOG_LEVEL}")
