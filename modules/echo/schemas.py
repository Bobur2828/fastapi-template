"""
Схемы для echo модуля
Pydantic модели для входных и выходных данных
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from shared.schemas.common import BaseSchema


class EchoBase(BaseModel):
    """Базовые поля echo"""
    message: str = Field(..., min_length=1, max_length=1000, description="Сообщение")
    category: Optional[str] = Field(None, max_length=100, description="Категория")


class EchoCreate(EchoBase):
    """Схема создания echo"""
    pass


class EchoUpdate(BaseModel):
    """Схема обновления echo"""
    message: Optional[str] = Field(None, min_length=1, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)


class EchoResponse(BaseSchema):
    """Ответ с данными echo"""
    message: str
    category: Optional[str]
    processed_message: str
    is_protected: bool = False
    
    class Config:
        from_attributes = True


class EchoRequest(BaseModel):
    """Запрос для обработки echo"""
    message: str = Field(..., min_length=1, max_length=1000)
    options: Optional[dict] = Field(None, description="Дополнительные опции")
