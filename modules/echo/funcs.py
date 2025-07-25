"""
Echo moduli uchun yordamchi funksiyalar
Ma’lumotlarni qayta ishlash mantiği
"""

from typing import Optional
from loguru import logger


def process_message(message: str) -> str:
    """
    Xabarni qayta ishlash
    Misol: matnni teskari aylantirish
    """
    if not message:
        return ""
    
    # Oddiy qayta ishlash — matnni teskari aylantirish
    processed = message[::-1]
    
    logger.debug(f"Qayta ishlangan xabar: {message[:20]}... -> {processed[:20]}...")
    return processed


def validate_category(category: Optional[str]) -> bool:
    """
    Kategoriya nomini tekshirish (validadsiya)
    Ruxsat etilganlar: general, test, demo, important
    """
    if not category:
        return True  # Kategoriya ixtiyoriy bo‘lishi mumkin
    
    allowed_categories = ["general", "test", "demo", "important"]
    return category.lower() in allowed_categories


def format_response(message: str, processed: str) -> dict:
    """
    API javobini formatlash
    """
    return {
        "original": message,
        "processed": processed,
        "length": len(message),
        "processed_length": len(processed)
    }
