"""
Ishlab chiqish va prodakshen uchun CORS sozlamalari
"""

from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings


def get_cors_middleware():
    """Sozlangan CORS middleware-ni qaytaradi"""
    return CORSMiddleware(
        allow_origins=settings.ALLOWED_ORIGINS,  # Ruxsat berilgan domenlar ro'yxati
        allow_credentials=True,  # Cookie va header orqali autentifikatsiyani qo‘llab-quvvatlaydi
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],  # Ruxsat berilgan HTTP metodlar
        allow_headers=["*"],  # Har qanday header'ga ruxsat
        expose_headers=["X-Process-Time", "X-Request-ID"],  # Javobda ko‘rsatiladigan maxsus headerlar
    )
