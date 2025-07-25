"""
Global xatoliklarni qayta ishlovchi middleware
Barcha qayta ishlanmagan istisnolarni ushlab, chiroyli javob qaytaradi
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

from core.settings import settings


async def error_handler_middleware(request: Request, call_next):
    """Barcha xatoliklarni ushlash uchun middleware"""
    try:
        response = await call_next(request)
        return response

    except HTTPException as e:
        # FastAPI tomonidan ko‘tarilgan istisnolar
        logger.warning(f"HTTP istisno: {e.status_code} - {e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content={
                "status": "error",
                "message": e.detail,
                "error_code": e.status_code
            }
        )

    except Exception as e:
        # Boshqa barcha xatoliklar
        logger.error(f"Qayta ishlanmagan xatolik: {str(e)}", exc_info=True)

        # Debug rejimida qo‘shimcha ma'lumot qaytariladi
        error_detail = {
            "status": "error",
            "message": "Ichki server xatosi",
            "error_code": 500
        }

        if settings.DEBUG:
            error_detail["details"] = str(e)
            error_detail["type"] = type(e).__name__

        return JSONResponse(
            status_code=500,
            content=error_detail
        )
