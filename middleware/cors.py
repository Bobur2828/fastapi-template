"""
Настройки CORS для разработки и продакшена
"""

from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings


def get_cors_middleware():
    """Возвращает настроенный CORS middleware"""
    return CORSMiddleware(
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time", "X-Request-ID"],
    )
