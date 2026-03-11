from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.db import get_db
from ..services.order_service import OrderService
from ..schemas.order_schema import OrderCreate, OrderResponse, OrderBookResponse
from ..schemas.trade_schema import TradeResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    try:
        return order_service.create_order(order_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    order = order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/user/{user_id}", response_model=List[OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.get_user_orders(user_id)

@router.delete("/{order_id}", response_model=OrderResponse)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    try:
        order = order_service.cancel_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orderbook/{symbol}", response_model=OrderBookResponse)
def get_order_book(symbol: str, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.get_order_book(symbol)

@router.get("/trades/all", response_model=List[TradeResponse])
def get_all_trades(db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.get_all_trades()

@router.get("/trades/{symbol}", response_model=List[TradeResponse])
def get_trades_by_symbol(symbol: str, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.get_trades_by_symbol(symbol)
