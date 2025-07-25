from sqlalchemy import Column, String, Text, Boolean
from core.db import BaseModel



class Contacs(BaseModel):
    __table__ = "contacts"

    phone = Column(String,nullable=False,comment="Foydalanuvchi telefon raqami")
    name = Column(String,nullable=False,comment="Foydalanuvchi ismi sharifi")

    def __repr__(self):
        return f"{self.name}=={self.phone}"
    