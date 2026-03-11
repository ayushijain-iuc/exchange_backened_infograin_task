from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    balance: float

class UserResponse(BaseModel):
    id: int
    name: str
    balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True
