from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..database.db import Base

class OrderSide(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(enum.Enum):
    OPEN = "OPEN"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    remaining_quantity = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.OPEN)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="orders")
    buy_trades = relationship("Trade", foreign_keys="Trade.buy_order_id", back_populates="buy_order")
    sell_trades = relationship("Trade", foreign_keys="Trade.sell_order_id", back_populates="sell_order")
    
    def __repr__(self):
        return f"<Order(id={self.id}, symbol={self.symbol}, side={self.side}, price={self.price}, quantity={self.quantity}, status={self.status})>"
