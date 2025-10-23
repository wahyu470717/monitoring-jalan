from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status
from app.repository.auth_repository import AuthRepository
from app.api.schemas.auth_schema import UserCreate, UserLogin, ActivityLogCreate
from app.utils.auth import verify_password, get_password_hash, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.repository = AuthRepository(db)
    
    def register_user(self, user: UserCreate):
        # Check if username exists
        existing_user = self.repository.get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email exists
        existing_email = self.repository.get_user_by_email(user.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        hashed_password = get_password_hash(user.password)
        return self.repository.create_user(user, hashed_password)
    
    def authenticate_user(self, login: UserLogin):
        user = self.repository.get_user_by_username(login.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        if not verify_password(login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "user": user}
    
    def log_activity(self, user_id: int, log: ActivityLogCreate):
        return self.repository.create_activity_log(user_id, log)
    
    def get_activity_logs(self, skip: int = 0, limit: int = 100):
        return self.repository.get_activity_logs(skip, limit)
    
    def get_user_activity_logs(self, user_id: int, skip: int = 0, limit: int = 100):
        return self.repository.get_user_activity_logs(user_id, skip, limit)