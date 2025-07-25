"""
Echo moduliga oid istisno holatlar (xatoliklar)
"""

from fastapi import HTTPException, status


class EchoException(HTTPException):
    """Echo moduli uchun asosiy (bazaviy) istisno"""
    pass


class EchoNotFoundError(EchoException):
    """Echo topilmagan holatdagi xatolik"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Echo topilmadi"
        )


class EchoValidationError(EchoException):
    """Kiritilgan ma'lumot noto‘g‘ri bo‘lsa (validadsiya xatosi)"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class EchoAccessDeniedError(EchoException):
    """Foydalanuvchida ruxsat bo‘lmaganda (access denied)"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ruxsat yo‘q"
        )
