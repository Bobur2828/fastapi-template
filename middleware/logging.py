"""
Middleware для логирования запросов
Записывает все входящие запросы и исходящие ответы
"""

import time
from fastapi import Request
from loguru import logger


async def logging_middleware(request: Request, call_next):
    """Middleware для логирования всех запросов"""
    start_time = time.time()
    
    # Получаем IP адрес клиента
    client_ip = request.client.host if request.client else "unknown"
    
    # Логируем входящий запрос
    logger.info(
        f"→ {request.method} {request.url.path} "
        f"from {client_ip} "
        f"User-Agent: {request.headers.get('user-agent', 'unknown')}"
    )
    
    # Обрабатываем запрос
    response = await call_next(request)
    
    # Время обработки
    process_time = time.time() - start_time
    
    # Логируем ответ
    log_level = "info"
    if response.status_code >= 400:
        log_level = "warning"
    if response.status_code >= 500:
        log_level = "error"
    
    getattr(logger, log_level)(
        f"← {request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"in {process_time:.3f}s"
    )
    
    # Добавляем заголовки ответа
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = str(id(request))  # Простой ID запроса
    
    return response
