from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.user_model import User
from ..schemas.user_schema import UserCreate, UserResponse

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        db_user = User(
            name=user_data.name,
            balance=user_data.balance
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserResponse.from_orm(db_user)
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            return UserResponse.from_orm(db_user)
        return None
    
    def get_all_users(self) -> List[UserResponse]:
        db_users = self.db.query(User).all()
        return [UserResponse.from_orm(user) for user in db_users]
    
    def update_user_balance(self, user_id: int, new_balance: float) -> Optional[UserResponse]:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.balance = new_balance
            self.db.commit()
            self.db.refresh(db_user)
            return UserResponse.from_orm(db_user)
        return None
