from pydantic import BaseModel
from datetime import datetime

class TradeResponse(BaseModel):
    id: int
    buy_order_id: int
    sell_order_id: int
    price: float
    quantity: int
    executed_at: datetime
    
    class Config:
        from_attributes = True
