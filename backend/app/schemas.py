from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool
    class Config:
        from_attributes = True

class RegisterIn(BaseModel):
    username: str
    password: str

class LoginIn(BaseModel):
    username: str
    password: str

class AuthOut(BaseModel):
    token: str
    user: UserOut

class ProductOut(BaseModel):
    id: int
    title: str
    brand: str
    price: float
    type: str
    description: str
    image_url: str
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    title: str
    brand: str
    price: float
    type: str
    description: str = ""

class CreateOrderItem(BaseModel):
    product_id: int
    quantity: int

class CreateOrderIn(BaseModel):
    items: List[CreateOrderItem]
    comment: str = ""

class OrderOut(BaseModel):
    id: int
    created_at: datetime
    status: str
    total: float
    class Config:
        from_attributes = True

class OrderItemOut(BaseModel):
    product_id: int
    title_snapshot: str
    price_snapshot: float
    quantity: int
