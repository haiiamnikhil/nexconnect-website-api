from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    tag: Optional[str] = None
    accent_color: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactMessageResponse(ContactMessageCreate):
    id: int
    created_at: datetime
    status: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AdminUserCreate(BaseModel):
    username: str
    password: str

class AdminUserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
