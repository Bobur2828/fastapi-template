"""
Сервисы для echo модуля
Бизнес-логика и работа с базой данных
"""

from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger

from shared.schemas.common import PaginationParams
from .models import Echo
from .schemas import EchoCreate, EchoResponse
from .funcs import process_message
from .exceptions import EchoNotFoundError


class EchoService:
    """Сервис для работы с echo"""
    
    async def get_all(
        self, 
        db: AsyncSession, 
        pagination: PaginationParams
    ) -> Tuple[List[EchoResponse], int]:
        """Получить все echo с пагинацией"""
        # Запрос с пагинацией
        query = select(Echo).where(
            Echo.deleted_at.is_(None)
        ).offset(pagination.skip).limit(pagination.limit)
        
        result = await db.execute(query)
        items = result.scalars().all()
        
        # Общее количество
        count_query = select(func.count(Echo.id)).where(
            Echo.deleted_at.is_(None)
        )
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Преобразование в схемы
        response_items = []
        for item in items:
            response_items.append(EchoResponse(
                id=item.id,
                created_at=item.created_at,
                updated_at=item.updated_at,
                message=item.message,
                category=item.category,
                processed_message=item.processed_message,
                is_protected=item.is_protected
            ))
        
        logger.info(f"Retrieved {len(response_items)} echos")
        return response_items, total
    
    async def get_by_id(self, db: AsyncSession, item_id: str) -> EchoResponse:
        """Получить echo по ID"""
        query = select(Echo).where(
            Echo.id == item_id,
            Echo.deleted_at.is_(None)
        )
        result = await db.execute(query)
        item = result.scalar_one_or_none()
        
        if not item:
            raise EchoNotFoundError()
        
        return EchoResponse(
            id=item.id,
            created_at=item.created_at,
            updated_at=item.updated_at,
            message=item.message,
            category=item.category,
            processed_message=item.processed_message,
            is_protected=item.is_protected
        )
    
    async def create(
        self, 
        db: AsyncSession, 
        data: EchoCreate,
        is_protected: bool = False
    ) -> EchoResponse:
        """Создать новый echo"""
        # Обработка сообщения
        processed_message = process_message(data.message)
        
        # Создание модели
        item = Echo(
            message=data.message,
            category=data.category,
            processed_message=processed_message,
            is_protected=is_protected
        )
        
        db.add(item)
        await db.commit()
        await db.refresh(item)
        
        logger.info(f"Created echo with ID: {item.id}")
        
        return EchoResponse(
            id=item.id,
            created_at=item.created_at,
            updated_at=item.updated_at,
            message=item.message,
            category=item.category,
            processed_message=item.processed_message,
            is_protected=item.is_protected
        )
    
    async def delete(self, db: AsyncSession, item_id: str) -> bool:
        """Мягкое удаление echo"""
        query = select(Echo).where(
            Echo.id == item_id,
            Echo.deleted_at.is_(None)
        )
        result = await db.execute(query)
        item = result.scalar_one_or_none()
        
        if not item:
            raise EchoNotFoundError()
        
        item.soft_delete()
        await db.commit()
        
        logger.info(f"Soft deleted echo with ID: {item_id}")
        return True


# Singleton instance
echo_service = EchoService()
