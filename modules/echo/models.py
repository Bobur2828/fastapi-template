"""
Echo moduli uchun DB modellari
SQLAlchemy ORM modeli
"""

from sqlalchemy import Column, String, Text, Boolean
from core.db import BaseModel


class Echo(BaseModel):
    """Echo modeli"""
    __tablename__ = "echo_items"  # Jadval nomi

    message = Column(Text, nullable=False, comment="Kiruvchi xabar")
    category = Column(String(100), nullable=True, comment="Kategoriya")
    processed_message = Column(Text, nullable=False, comment="Qayta ishlangan xabar")
    is_protected = Column(Boolean, default=False, comment="Himoyalangan endpoint orqali yaratilgan")

    def __repr__(self):
        return f"<Echo(id={self.id}, message={self.message[:50]})>"
