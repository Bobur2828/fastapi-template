from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from core.dependencies import get_db, verify_bearer_token
from shared.schemas.common import ResponseModel, PaginatedResponse, PaginationParams
from .schemas import EchoRequest, EchoResponse, EchoCreate
from .services import echo_service
from .exceptions import EchoNotFoundError

router = APIRouter()



@router.get("progas")



@router.get("/", response_model=PaginatedResponse[EchoResponse])
async def get_echos(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех echo"""
    try:
        items, total = await echo_service.get_all(db, pagination)
        return PaginatedResponse.create(items, total, pagination)
    except Exception as e:
        logger.error(f"Error getting echos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve echos"
        )