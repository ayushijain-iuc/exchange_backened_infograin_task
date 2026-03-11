from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.db import get_db
from ..services.user_service import UserService
from ..schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if user_data.balance < 0:
        raise HTTPException(status_code=400, detail="Balance cannot be negative")
    
    user_service = UserService(db)
    return user_service.create_user(user_data)

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
