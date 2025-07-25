"""
Ilovaning umumiy bog‘liqliklari
FastAPI da Dependency Injection orqali ishlatiladi
"""

from typing import AsyncGenerator
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from core.settings import settings
from core.db import SessionLocal

# Bearer xavfsizlik sxemasi
security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Ma'lumotlar bazasi sessiyasini olish
    Foydalanishdan keyin avtomatik yopiladi
    """
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Ma'lumotlar bazasi sessiyasi xatoligi: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Bearer tokenni tekshirish
    Faqat himoyalangan endpointlarda ishlatiladi
    """
    if credentials.credentials != settings.BEARER_TOKEN:
        logger.warning(f"Noto‘g‘ri bearer token urinishlari: {credentials.credentials[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Noto‘g‘ri bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


async def get_current_user_id(
    token: str = Depends(verify_bearer_token)
) -> str:
    """
    Hozirgi foydalanuvchi ID sini olish
    Kelajakda autentifikatsiya tizimi uchun asos
    """
    # TODO: Token asosida foydalanuvchini aniqlashni amalga oshirish
    return "system_user"
