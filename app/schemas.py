from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    category: str
    color: str
    sizes: str  # JSON string
    images: str  # JSON string
    stock: int
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: Optional[str] = None
    color: Optional[str] = None
    sizes: Optional[str] = None
    images: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Order schemas
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    size: str
    color: str

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    customer_address: str
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    product_code: str
    quantity: int
    price: float
    size: str
    color: str
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    transaction_id: str
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_address: str
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None