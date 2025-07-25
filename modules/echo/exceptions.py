"""
Исключения для echo модуля
"""

from fastapi import HTTPException, status


class EchoException(HTTPException):
    """Базовое исключение для echo модуля"""
    pass


class EchoNotFoundError(EchoException):
    """Исключение когда echo не найден"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Echo not found"
        )


class EchoValidationError(EchoException):
    """Ошибка валидации данных"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class EchoAccessDeniedError(EchoException):
    """Ошибка доступа"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
