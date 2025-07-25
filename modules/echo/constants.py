"""
Константы для echo модуля
"""

# Ограничения
MAX_MESSAGE_LENGTH = 1000
MIN_MESSAGE_LENGTH = 1
MAX_CATEGORY_LENGTH = 100

# Категории
ALLOWED_CATEGORIES = [
    "general",
    "test", 
    "demo",
    "important"
]

# Статусы
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_DELETED = "deleted"

# Сообщения
MSG_CREATED = f"Echo created successfully"
MSG_UPDATED = f"Echo updated successfully"
MSG_DELETED = f"Echo deleted successfully"
MSG_NOT_FOUND = f"Echo not found"
