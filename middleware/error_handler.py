"""
Глобальный обработчик ошибок
Ловит все необработанные исключения и возвращает красивый ответ
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

from core.settings import settings


async def error_handler_middleware(request: Request, call_next):
    """Middleware для обработки всех ошибок"""
    try:
        response = await call_next(request)
        return response
    
    except HTTPException as e:
        # FastAPI исключения
        logger.warning(f"HTTP Exception: {e.status_code} - {e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content={
                "status": "error",
                "message": e.detail,
                "error_code": e.status_code
            }
        )
    
    except Exception as e:
        # Все остальные ошибки
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        
        # Детальная информация только в debug режиме
        error_detail = {
            "status": "error",
            "message": "Internal server error",
            "error_code": 500
        }
        
        if settings.DEBUG:
            error_detail["details"] = str(e)
            error_detail["type"] = type(e).__name__
        
        return JSONResponse(
            status_code=500,
            content=error_detail
        )
