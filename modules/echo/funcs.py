"""
Вспомогательные функции для echo модуля
Логика обработки данных
"""

from typing import Optional
from loguru import logger


def process_message(message: str) -> str:
    """
    Обработка сообщения
    Пример: переворачивание строки
    """
    if not message:
        return ""
    
    # Простая обработка - переворачивание
    processed = message[::-1]
    
    logger.debug(f"Processed message: {message[:20]}... -> {processed[:20]}...")
    return processed


def validate_category(category: Optional[str]) -> bool:
    """Валидация категории"""
    if not category:
        return True
    
    allowed_categories = ["general", "test", "demo", "important"]
    return category.lower() in allowed_categories


def format_response(message: str, processed: str) -> dict:
    """Форматирование ответа"""
    return {
        "original": message,
        "processed": processed,
        "length": len(message),
        "processed_length": len(processed)
    }
