"""
Базовые модели для наследования
"""

from typing import Optional, List, Any, Dict
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from core.db import BaseModel


class TimestampedMixin:
    """Миксин для моделей с временными метками"""
    # Уже есть в BaseModel: created_at, updated_at
    pass


class SoftDeleteMixin:
    """Миксин для мягкого удаления"""
    # Уже есть в BaseModel: deleted_at
    pass


class NamedMixin:
    """Миксин для моделей с названием"""
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class StatusMixin:
    """Миксин для моделей со статусом"""
    is_active = Column(Boolean, default=True)
    status = Column(String(50), default="active")


class MetadataMixin:
    """Миксин для дополнительных данных"""
    # Можно добавить JSON поле для метаданных
    # metadata = Column(JSON, nullable=True)
    pass


class AuditMixin:
    """Миксин для аудита изменений"""
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    
    @declared_attr
    def created_by_user(cls):
        # Связь с таблицей пользователей (когда она будет)
        # return relationship("User", foreign_keys=[cls.created_by])
        pass
