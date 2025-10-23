from sqlalchemy.orm import Session
from typing import Optional
from app.domain.models import User, ActivityLog
from app.api.schemas.auth_schema import UserCreate, ActivityLogCreate

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def create_activity_log(self, user_id: int, log: ActivityLogCreate) -> ActivityLog:
        db_log = ActivityLog(
            user_id=user_id,
            action=log.action,
            entity_type=log.entity_type,
            entity_id=log.entity_id,
            description=log.description,
            ip_address=log.ip_address,
            user_agent=log.user_agent
        )
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log
    
    def get_activity_logs(self, skip: int = 0, limit: int = 100):
        return self.db.query(ActivityLog).order_by(
            ActivityLog.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_user_activity_logs(self, user_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(ActivityLog).filter(
            ActivityLog.user_id == user_id
        ).order_by(
            ActivityLog.created_at.desc()
        ).offset(skip).limit(limit).all()