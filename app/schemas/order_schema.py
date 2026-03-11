from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ..models.order_model import OrderSide, OrderStatus

class OrderCreate(BaseModel):
    user_id: int
    symbol: str
    side: OrderSide
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)

class OrderResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    side: OrderSide
    price: float
    quantity: int
    remaining_quantity: int
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OrderBookEntry(BaseModel):
    price: float
    quantity: int
    order_count: int

class OrderBookResponse(BaseModel):
    symbol: str
    buy_orders: list[OrderBookEntry]
    sell_orders: list[OrderBookEntry]
