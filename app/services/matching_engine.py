from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from ..models.order_model import Order, OrderSide, OrderStatus
from ..models.trade_model import Trade
from ..models.user_model import User
import asyncio
from threading import Lock

class MatchingEngine:
    def __init__(self, db: Session):
        self.db = db
        self._lock = Lock()
    
    def match_order(self, new_order: Order) -> List[Trade]:
        with self._lock:
            trades = []
            
            if new_order.side == OrderSide.BUY:
                trades = self._match_buy_order(new_order)
            else:
                trades = self._match_sell_order(new_order)
            
            self._update_order_status(new_order)
            return trades
    
    def _match_buy_order(self, buy_order: Order) -> List[Trade]:
        trades = []
        
        sell_orders = self.db.query(Order).filter(
            Order.symbol == buy_order.symbol,
            Order.side == OrderSide.SELL,
            Order.status == OrderStatus.OPEN,
            Order.price <= buy_order.price
        ).order_by(Order.price.asc(), Order.created_at.asc()).all()
        
        for sell_order in sell_orders:
            if buy_order.remaining_quantity <= 0:
                break
            
            # Prevent self-matching
            if buy_order.user_id == sell_order.user_id:
                continue
            
            trade_quantity = min(buy_order.remaining_quantity, sell_order.remaining_quantity)
            
            trade = Trade(
                buy_order_id=buy_order.id,
                sell_order_id=sell_order.id,
                price=sell_order.price,
                quantity=trade_quantity
            )
            
            self.db.add(trade)
            trades.append(trade)
            
            buy_order.remaining_quantity -= trade_quantity
            sell_order.remaining_quantity -= trade_quantity
            
            if sell_order.remaining_quantity <= 0:
                sell_order.status = OrderStatus.FILLED
            else:
                sell_order.status = OrderStatus.PARTIALLY_FILLED
            
            self.db.commit()
        
        return trades
    
    def _match_sell_order(self, sell_order: Order) -> List[Trade]:
        trades = []
        
        buy_orders = self.db.query(Order).filter(
            Order.symbol == sell_order.symbol,
            Order.side == OrderSide.BUY,
            Order.status == OrderStatus.OPEN,
            Order.price >= sell_order.price
        ).order_by(Order.price.desc(), Order.created_at.asc()).all()
        
        for buy_order in buy_orders:
            if sell_order.remaining_quantity <= 0:
                break
            
            # Prevent self-matching
            if buy_order.user_id == sell_order.user_id:
                continue
            
            trade_quantity = min(sell_order.remaining_quantity, buy_order.remaining_quantity)
            
            trade = Trade(
                buy_order_id=buy_order.id,
                sell_order_id=sell_order.id,
                price=buy_order.price,
                quantity=trade_quantity
            )
            
            self.db.add(trade)
            trades.append(trade)
            
            sell_order.remaining_quantity -= trade_quantity
            buy_order.remaining_quantity -= trade_quantity
            
            if buy_order.remaining_quantity <= 0:
                buy_order.status = OrderStatus.FILLED
            else:
                buy_order.status = OrderStatus.PARTIALLY_FILLED
            
            self.db.commit()
        
        return trades
    
    def _update_order_status(self, order: Order):
        if order.remaining_quantity <= 0:
            order.status = OrderStatus.FILLED
        elif order.remaining_quantity < order.quantity:
            order.status = OrderStatus.PARTIALLY_FILLED
        else:
            order.status = OrderStatus.OPEN
        
        self.db.commit()
