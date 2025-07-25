"""
Модели БД для echo модуля
SQLAlchemy модели
"""

from sqlalchemy import Column, String, Text, Boolean

from core.db import BaseModel


class Echo(BaseModel):
    """Модель echo"""
    __tablename__ = "echo_items"
    
    message = Column(Text, nullable=False, comment="Исходное сообщение")
    category = Column(String(100), nullable=True, comment="Категория")
    processed_message = Column(Text, nullable=False, comment="Обработанное сообщение")
    is_protected = Column(Boolean, default=False, comment="Создано через защищенный эндпоинт")
    
    def __repr__(self):
        return f"<Echo(id={self.id}, message={self.message[:50]})>"
