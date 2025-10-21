from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.service.jalan_service import JalanService
from app.api.schemas.jalan_schema import Jalan, JalanCreate, JalanUpdate

router = APIRouter(prefix="/api/jalan", tags=["jalan"])

@router.get("/", response_model=List[Jalan])
def get_all_jalan(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    service = JalanService(db)
    return service.get_all_jalan(skip, limit)

@router.get("/{jalan_id}", response_model=Jalan)
def get_jalan(jalan_id: int, db: Session = Depends(get_db)):
    service = JalanService(db)
    jalan = service.get_jalan_by_id(jalan_id)
    if not jalan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jalan tidak ditemukan"
        )
    return jalan

@router.post("/", response_model=Jalan)
def create_jalan(jalan: JalanCreate, db: Session = Depends(get_db)):
    service = JalanService(db)
    return service.create_jalan(jalan)

@router.put("/{jalan_id}", response_model=Jalan)
def update_jalan(jalan_id: int, jalan: JalanUpdate, db: Session = Depends(get_db)):
    service = JalanService(db)
    updated_jalan = service.update_jalan(jalan_id, jalan)
    if not updated_jalan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jalan tidak ditemukan"
        )
    return updated_jalan

@router.delete("/{jalan_id}")
def delete_jalan(jalan_id: int, db: Session = Depends(get_db)):
    service = JalanService(db)
    success = service.delete_jalan(jalan_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jalan tidak ditemukan"
        )
    return {"message": "Jalan berhasil dihapus"}

@router.get("/kondisi/{kondisi}", response_model=List[Jalan])
def get_jalan_by_kondisi(kondisi: str, db: Session = Depends(get_db)):
    service = JalanService(db)
    return service.get_jalan_by_kondisi(kondisi)

@router.get("/kecamatan/{kecamatan}", response_model=List[Jalan])
def get_jalan_by_kecamatan(kecamatan: str, db: Session = Depends(get_db)):
    service = JalanService(db)
    return service.get_jalan_by_kecamatan(kecamatan)