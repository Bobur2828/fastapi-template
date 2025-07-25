"""
Model meros olish uchun asosiy mikslarga oid klasslar
"""

from typing import Optional, List, Any, Dict
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from core.db import BaseModel


class TimestampedMixin:
    """Vaqt muhrlari bilan ishlovchi modellar uchun mixin"""
    # BaseModel'da mavjud: created_at, updated_at
    pass


class SoftDeleteMixin:
    """Yumshoq o‘chirish (soft delete) uchun mixin"""
    # BaseModel'da mavjud: deleted_at
    pass


class NamedMixin:
    """Nom va tavsifga ega modellar uchun mixin"""
    name = Column(String(255), nullable=False)  # Majburiy nom
    description = Column(Text, nullable=True)   # Ixtiyoriy tavsif


class StatusMixin:
    """Status va aktivlik holati uchun mixin"""
    is_active = Column(Boolean, default=True)         # Foydalanish holati
    status = Column(String(50), default="active")     # Status matni


class MetadataMixin:
    """Qo‘shimcha meta-ma’lumotlar uchun mixin"""
    # Meta ma’lumotlar uchun JSON ustun qo‘shish mumkin
    # metadata = Column(JSON, nullable=True)
    pass


class AuditMixin:
    """O‘zgarishlar tarixini kuzatish uchun audit mixin"""
    created_by = Column(String(255), nullable=True)  # Kim yaratgan
    updated_by = Column(String(255), nullable=True)  # Kim tahrirlagan
    
    @declared_attr
    def created_by_user(cls):
        # Foydalanuvchi jadvali bilan bog‘lash (kelajakda kerak bo‘lsa)
        # return relationship("User", foreign_keys=[cls.created_by])
        pass
