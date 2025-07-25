"""
So‘rovlarni loglash uchun middleware
Barcha kiruvchi so‘rovlar va chiqish javoblarini yozib boradi
"""

import time
from fastapi import Request
from loguru import logger


async def logging_middleware(request: Request, call_next):
    """Barcha so‘rovlarni loglash uchun middleware"""
    start_time = time.time()
    
    # Mijozning IP manzilini olish
    client_ip = request.client.host if request.client else "nomalum"
    
    # Kiruvchi so‘rovni loglash
    logger.info(
        f"→ {request.method} {request.url.path} "
        f"mijoz: {client_ip} "
        f"User-Agent: {request.headers.get('user-agent', 'nomalum')}"
    )
    
    # So‘rovni qayta ishlash
    response = await call_next(request)
    
    # Qayta ishlash vaqti (sekundda)
    process_time = time.time() - start_time
    
    # Chiquvchi javobni loglash
    log_level = "info"
    if response.status_code >= 400:
        log_level = "warning"
    if response.status_code >= 500:
        log_level = "error"
    
    getattr(logger, log_level)(
        f"← {request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"{process_time:.3f} soniyada bajarildi"
    )
    
    # Javobga qo‘shimcha sarlavhalar qo‘shamiz
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = str(id(request))  # Oddiy so‘rov ID
    
    return response
