from typing import List, Optional
from sqlalchemy.orm import Session
from app.repository.jalan_repository import JalanRepository
from app.api.schemas.jalan_schema import JalanCreate, JalanUpdate, DashboardStats

class JalanService:
    def __init__(self, db: Session):
        self.repository = JalanRepository(db)
    
    def get_all_jalan(self, skip: int = 0, limit: int = 100) -> List[JalanCreate]:
        return self.repository.get_all(skip, limit)
    
    def get_jalan_by_id(self, jalan_id: int) -> Optional[JalanCreate]:
        return self.repository.get_by_id(jalan_id)
    
    def create_jalan(self, jalan: JalanCreate) -> JalanCreate:
        return self.repository.create(jalan)
    
    def update_jalan(self, jalan_id: int, jalan: JalanUpdate) -> Optional[JalanCreate]:
        return self.repository.update(jalan_id, jalan)
    
    def delete_jalan(self, jalan_id: int) -> bool:
        return self.repository.delete(jalan_id)
    
    def get_jalan_by_kondisi(self, kondisi: str) -> List[JalanCreate]:
        return self.repository.get_by_kondisi(kondisi)
    
    def get_jalan_by_kecamatan(self, kecamatan: str) -> List[JalanCreate]:
        return self.repository.get_by_kecamatan(kecamatan)
    
    def get_dashboard_stats(self) -> DashboardStats:
        stats = self.repository.get_dashboard_stats()
        return DashboardStats(**stats)