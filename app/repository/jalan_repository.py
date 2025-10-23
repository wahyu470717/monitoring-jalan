from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.domain.models import Jalan
from app.api.schemas.jalan_schema import JalanCreate, JalanUpdate

class JalanRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Jalan]:
        return self.db.query(Jalan).filter(Jalan.is_active == True).offset(skip).limit(limit).all()
    
    def get_by_id(self, jalan_id: int) -> Optional[Jalan]:
        return self.db.query(Jalan).filter(Jalan.id == jalan_id, Jalan.is_active == True).first()
    
    def create(self, jalan: JalanCreate) -> Jalan:
        db_jalan = Jalan(**jalan.dict())
        self.db.add(db_jalan)
        self.db.commit()
        self.db.refresh(db_jalan)
        return db_jalan
    
    def update(self, jalan_id: int, jalan: JalanUpdate) -> Optional[Jalan]:
        db_jalan = self.get_by_id(jalan_id)
        if db_jalan:
            for key, value in jalan.dict().items():
                setattr(db_jalan, key, value)
            self.db.commit()
            self.db.refresh(db_jalan)
        return db_jalan
    
    def delete(self, jalan_id: int) -> bool:
        db_jalan = self.get_by_id(jalan_id)
        if db_jalan:
            db_jalan.is_active = False
            self.db.commit()
            return True
        return False
    
    def get_by_kondisi(self, kondisi: str) -> List[Jalan]:
        return self.db.query(Jalan).filter(
            Jalan.kondisi == kondisi, 
            Jalan.is_active == True
        ).all()
    
    def get_by_kecamatan(self, kecamatan: str) -> List[Jalan]:
        return self.db.query(Jalan).filter(
            Jalan.kecamatan == kecamatan,
            Jalan.is_active == True
        ).all()