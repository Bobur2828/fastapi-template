"""
Настройка логирования через loguru
Один раз настроить здесь, потом везде просто импортить logger
"""

import sys
from pathlib import Path
from loguru import logger

from core.settings import settings


def setup_logging():
    """Настройка логирования для приложения"""
    # Удаляем стандартный handler
    logger.remove()
    
    # Создаем папку для логов если её нет
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Формат логов
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Консольный вывод
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.DEBUG else settings.LOG_LEVEL,
        colorize=True,
    )
    
    # Файловый вывод
    logger.add(
        settings.LOG_FILE,
        format=log_format,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        level=settings.LOG_LEVEL,
        encoding="utf-8",
    )
    
    # Отдельный файл для ошибок
    logger.add(
        settings.LOG_FILE.replace(".log", "_errors.log"),
        format=log_format,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
    )
    
    logger.info(f"Логирование настроено. Debug: {settings.DEBUG}, Level: {settings.LOG_LEVEL}")
