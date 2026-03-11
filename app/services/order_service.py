from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.order_model import Order, OrderSide, OrderStatus
from ..models.trade_model import Trade
from ..schemas.order_schema import OrderCreate, OrderResponse, OrderBookResponse, OrderBookEntry
from ..schemas.trade_schema import TradeResponse
from .matching_engine import MatchingEngine

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.matching_engine = MatchingEngine(db)
    
    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        # Check if user exists
        from ..models.user_model import User
        user = self.db.query(User).filter(User.id == order_data.user_id).first()
        if not user:
            raise ValueError(f"User with ID {order_data.user_id} not found")
        
        # Validate balance for buy orders
        if order_data.side == OrderSide.BUY:
            required_balance = order_data.price * order_data.quantity
            if user.balance < required_balance:
                raise ValueError(f"Insufficient balance. Required: {required_balance}, Available: {user.balance}")
        
        db_order = Order(
            user_id=order_data.user_id,
            symbol=order_data.symbol,
            side=order_data.side,
            price=order_data.price,
            quantity=order_data.quantity,
            remaining_quantity=order_data.quantity,
            status=OrderStatus.OPEN
        )
        
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        
        trades = self.matching_engine.match_order(db_order)
        
        self.db.refresh(db_order)
        return OrderResponse.from_orm(db_order)
    
    def get_order_by_id(self, order_id: int) -> Optional[OrderResponse]:
        db_order = self.db.query(Order).filter(Order.id == order_id).first()
        if db_order:
            return OrderResponse.from_orm(db_order)
        return None
    
    def get_user_orders(self, user_id: int) -> List[OrderResponse]:
        db_orders = self.db.query(Order).filter(Order.user_id == user_id).all()
        return [OrderResponse.from_orm(order) for order in db_orders]
    
    def cancel_order(self, order_id: int) -> Optional[OrderResponse]:
        db_order = self.db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return None
        
        if db_order.status != OrderStatus.OPEN:
            raise ValueError("Only open orders can be cancelled")
        
        db_order.status = OrderStatus.CANCELLED
        self.db.commit()
        self.db.refresh(db_order)
        
        return OrderResponse.from_orm(db_order)
    
    def get_order_book(self, symbol: str) -> OrderBookResponse:
        buy_orders = self.db.query(Order).filter(
            Order.symbol == symbol,
            Order.side == OrderSide.BUY,
            Order.status == OrderStatus.OPEN
        ).order_by(Order.price.desc(), Order.created_at.asc()).all()
        
        sell_orders = self.db.query(Order).filter(
            Order.symbol == symbol,
            Order.side == OrderSide.SELL,
            Order.status == OrderStatus.OPEN
        ).order_by(Order.price.asc(), Order.created_at.asc()).all()
        
        buy_book = self._aggregate_orders_by_price(buy_orders)
        sell_book = self._aggregate_orders_by_price(sell_orders)
        
        return OrderBookResponse(
            symbol=symbol,
            buy_orders=buy_book,
            sell_orders=sell_book
        )
    
    def _aggregate_orders_by_price(self, orders: List[Order]) -> List[OrderBookEntry]:
        price_dict = {}
        
        for order in orders:
            if order.price not in price_dict:
                price_dict[order.price] = {"quantity": 0, "count": 0}
            price_dict[order.price]["quantity"] += order.remaining_quantity
            price_dict[order.price]["count"] += 1
        
        return [
            OrderBookEntry(
                price=price,
                quantity=data["quantity"],
                order_count=data["count"]
            )
            for price, data in sorted(price_dict.items(), 
                                    reverse=orders[0].side == OrderSide.BUY if orders else False)
        ]
    
    def get_all_trades(self) -> List[TradeResponse]:
        db_trades = self.db.query(Trade).order_by(Trade.executed_at.desc()).all()
        return [TradeResponse.from_orm(trade) for trade in db_trades]
    
    def get_trades_by_symbol(self, symbol: str) -> List[TradeResponse]:
        db_trades = self.db.query(Trade).join(Order, Trade.buy_order_id == Order.id).filter(
            Order.symbol == symbol
        ).order_by(Trade.executed_at.desc()).all()
        return [TradeResponse.from_orm(trade) for trade in db_trades]
