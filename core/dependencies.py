"""
Общие зависимости для всего приложения
Используются через Dependency Injection в FastAPI
"""

from typing import AsyncGenerator
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from core.settings import settings
from core.db import SessionLocal

# Bearer схема безопасности
security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Получение сессии БД
    Автоматически закрывается после использования
    """
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Проверка Bearer токена
    Используется только на защищенных эндпоинтах
    """
    if credentials.credentials != settings.BEARER_TOKEN:
        logger.warning(f"Invalid bearer token attempt: {credentials.credentials[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


async def get_current_user_id(
    token: str = Depends(verify_bearer_token)
) -> str:
    """
    Получение ID текущего пользователя
    Заглушка для будущей системы аутентификации
    """
    # TODO: Реализовать получение пользователя из токена
    return "system_user"
