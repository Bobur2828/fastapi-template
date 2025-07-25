"""
Ilovaning umumiy sxemalari
Javoblar, sahifalash (pagination) va boshqa umumiy modellar
"""

from typing import Generic, TypeVar, Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """Muvaffaqiyatli javob uchun asosiy model"""
    status: str = "ok"
    data: T
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Xatolik javobi uchun model"""
    status: str = "error"
    message: str
    error_code: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class PaginationParams(BaseModel):
    """Sahifalash parametrlar modeli"""
    page: int = Field(1, ge=1, description="Sahifa raqami")
    page_size: int = Field(20, ge=1, le=100, description="Sahifadagi elementlar soni")

    @property
    def skip(self) -> int:
        """Qancha elementni o'tkazib yuborish (offset)"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """So'rovdagi maksimal elementlar soni (limit)"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Sahifalangan javob modeli"""
    status: str = "ok"
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def create(cls, items: List[T], total: int, pagination: PaginationParams):
        """Sahifalangan javob yaratish"""
        pages = (total + pagination.page_size - 1) // pagination.page_size
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages
        )


class BaseSchema(BaseModel):
    """Umumiy maydonlarga ega asosiy sxema"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: str
        }


class HealthResponse(BaseModel):
    """Sog‘liqni tekshirish (health check) javobi"""
    status: str
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    uptime: Optional[float] = None


class CreateResponse(BaseModel):
    """Resurs yaratilgandagi javob"""
    status: str = "ok"
    message: str = "Resurs muvaffaqiyatli yaratildi"
    id: uuid.UUID


class UpdateResponse(BaseModel):
    """Resurs yangilanganidagi javob"""
    status: str = "ok"
    message: str = "Resurs muvaffaqiyatli yangilandi"
    id: uuid.UUID


class DeleteResponse(BaseModel):
    """Resurs o‘chirilgandagi javob"""
    status: str = "ok"
    message: str = "Resurs muvaffaqiyatli o‘chirildi"
    id: uuid.UUID
