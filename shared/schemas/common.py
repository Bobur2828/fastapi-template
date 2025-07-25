"""
Общие схемы для всего приложения
Базовые модели ответов, пагинация и тд
"""

from typing import Generic, TypeVar, Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """Базовая модель успешного ответа"""
    status: str = "ok"
    data: T
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Модель ошибки"""
    status: str = "error"
    message: str
    error_code: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class PaginationParams(BaseModel):
    """Параметры пагинации"""
    page: int = Field(1, ge=1, description="Номер страницы")
    page_size: int = Field(20, ge=1, le=100, description="Количество элементов на странице")
    
    @property
    def skip(self) -> int:
        """Количество элементов для пропуска"""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Лимит элементов для запроса"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Ответ с пагинацией"""
    status: str = "ok"
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    
    @classmethod
    def create(cls, items: List[T], total: int, pagination: PaginationParams):
        """Создать ответ с пагинацией"""
        pages = (total + pagination.page_size - 1) // pagination.page_size
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages
        )


class BaseSchema(BaseModel):
    """Базовая схема с общими полями"""
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
    """Ответ health check"""
    status: str
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    uptime: Optional[float] = None


class CreateResponse(BaseModel):
    """Ответ при создании ресурса"""
    status: str = "ok"
    message: str = "Resource created successfully"
    id: uuid.UUID


class UpdateResponse(BaseModel):
    """Ответ при обновлении ресурса"""
    status: str = "ok"
    message: str = "Resource updated successfully"
    id: uuid.UUID


class DeleteResponse(BaseModel):
    """Ответ при удалении ресурса"""
    status: str = "ok"
    message: str = "Resource deleted successfully"
    id: uuid.UUID
