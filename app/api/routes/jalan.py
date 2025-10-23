from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.service.jalan_service import JalanService
from app.service.auth_service import AuthService
from app.api.schemas.jalan_schema import Jalan, JalanCreate, JalanUpdate
from app.api.schemas.response_schemas import success_response, error_response
from app.api.schemas.auth_schema import ActivityLogCreate
from app.utils.auth import get_current_active_user
from app.domain.models import User

router = APIRouter(prefix="/api/jalan", tags=["jalan"])

def log_activity(db: Session, user: User, action: str, entity_id: int = None, description: str = None):
    """Helper function to log user activities"""
    auth_service = AuthService(db)
    log = ActivityLogCreate(
        action=action,
        entity_type="jalan",
        entity_id=entity_id,
        description=description
    )
    auth_service.log_activity(user.id, log)

@router.get("/")
def get_all_jalan(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        service = JalanService(db)
        jalan_list = service.get_all_jalan(skip, limit)
        
        if not jalan_list:
            return success_response(
                data=[],
                message="No data found"
            )
        
        return success_response(
            data=[Jalan.from_orm(jalan) for jalan in jalan_list],
            message="Data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/{jalan_id}")
def get_jalan(
    jalan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        service = JalanService(db)
        jalan = service.get_jalan_by_id(jalan_id)
        
        if not jalan:
            raise HTTPException(
                status_code=404,
                detail=error_response("Data not found", 404)
            )
        
        return success_response(
            data=Jalan.from_orm(jalan),
            message="Data retrieved successfully"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.post("/")
def create_jalan(
    jalan: JalanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        service = JalanService(db)
        new_jalan = service.create_jalan(jalan)
        
        # Log activity
        log_activity(
            db, current_user, "create",
            entity_id=new_jalan.id,
            description=f"Created jalan: {new_jalan.nama_jalan}"
        )
        
        return success_response(
            data=Jalan.from_orm(new_jalan),
            message="Data created successfully",
            code=201
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.put("/{jalan_id}")
def update_jalan(
    jalan_id: int,
    jalan: JalanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        service = JalanService(db)
        updated_jalan = service.update_jalan(jalan_id, jalan)
        
        if not updated_jalan:
            raise HTTPException(
                status_code=404,
                detail=error_response("Data not found", 404)
            )
        
        # Log activity
        log_activity(
            db, current_user, "update",
            entity_id=jalan_id,
            description=f"Updated jalan: {updated_jalan.nama_jalan}"
        )
        
        return success_response(
            data=Jalan.from_orm(updated_jalan),
            message="Data updated successfully"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.delete("/{jalan_id}")
def delete_jalan(
    jalan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        service = JalanService(db)
        
        # Get jalan name before deleting
        jalan = service.get_jalan_by_id(jalan_id)
        if not jalan:
            raise HTTPException(
                status_code=404,
                detail=error_response("Data not found", 404)
            )
        
        success = service.delete_jalan(jalan_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=error_response("Data not found", 404)
            )
        
        # Log activity
        log_activity(
            db, current_user, "delete",
            entity_id=jalan_id,
            description=f"Deleted jalan: {jalan.nama_jalan}"
        )
        
        return success_response(
            message="Data deleted successfully"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/kondisi/{kondisi}")
def get_jalan_by_kondisi(
    kondisi: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        service = JalanService(db)
        jalan_list = service.get_jalan_by_kondisi(kondisi)
        
        if not jalan_list:
            return success_response(
                data=[],
                message="No data found"
            )
        
        return success_response(
            data=[Jalan.from_orm(jalan) for jalan in jalan_list],
            message="Data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/kecamatan/{kecamatan}")
def get_jalan_by_kecamatan(
    kecamatan: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        service = JalanService(db)
        jalan_list = service.get_jalan_by_kecamatan(kecamatan)
        
        if not jalan_list:
            return success_response(
                data=[],
                message="No data found"
            )
        
        return success_response(
            data=[Jalan.from_orm(jalan) for jalan in jalan_list],
            message="Data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )