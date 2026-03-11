from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    orders = relationship("Order", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, balance={self.balance})>"
