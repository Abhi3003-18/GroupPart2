from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class OrderCreate(OrderBase):
    order_date: Optional[datetime] = Field(default_factory=datetime.utcnow)


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    order_details: List[OrderDetail] = None

    class Config:
        orm_mode = True
