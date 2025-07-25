"""
Echo модуль - роутер
API эндпоинты для echo функциональности
"""

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


@router.get("/{item_id}", response_model=ResponseModel[EchoResponse])
async def get_echo(
    item_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить echo по ID"""
    try:
        item = await echo_service.get_by_id(db, item_id)
        return ResponseModel(data=item)
    except EchoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Echo not found"
        )


@router.post("/", response_model=ResponseModel[EchoResponse])
async def create_echo(
    request: EchoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новый echo"""
    try:
        item = await echo_service.create(db, request)
        return ResponseModel(
            data=item,
            message=f"Echo created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating echo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create echo"
        )


@router.post("/protected", 
    response_model=ResponseModel[EchoResponse],
    dependencies=[Depends(verify_bearer_token)]
)
async def create_protected_echo(
    request: EchoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать echo (защищенный эндпоинт)"""
    try:
        item = await echo_service.create(db, request, is_protected=True)
        return ResponseModel(
            data=item,
            message=f"Protected echo created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating protected echo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create protected echo"
        )


@router.delete("/{item_id}", dependencies=[Depends(verify_bearer_token)])
async def delete_echo(
    item_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Удалить echo (мягкое удаление)"""
    try:
        await echo_service.delete(db, item_id)
        return ResponseModel(
            data={"id": item_id},
            message=f"Echo deleted successfully"
        )
    except EchoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Echo not found"
        )
