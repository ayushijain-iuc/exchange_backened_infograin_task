from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database.db import Base

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    buy_order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sell_order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    buy_order = relationship("Order", foreign_keys=[buy_order_id], back_populates="buy_trades")
    sell_order = relationship("Order", foreign_keys=[sell_order_id], back_populates="sell_trades")
    
    def __repr__(self):
        return f"<Trade(id={self.id}, buy_order_id={self.buy_order_id}, sell_order_id={self.sell_order_id}, price={self.price}, quantity={self.quantity})>"
