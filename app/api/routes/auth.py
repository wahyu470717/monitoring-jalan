from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.service.auth_service import AuthService
from app.api.schemas.auth_schema import (
    UserCreate, UserLogin, UserResponse, Token, 
    ActivityLogCreate, ActivityLogResponse
)
from app.api.schemas.response_schemas import success_response, error_response
from app.utils.auth import get_current_active_user
from app.domain.models import User

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        service = AuthService(db)
        new_user = service.register_user(user)
        return success_response(
            data=UserResponse.from_orm(new_user),
            message="User registered successfully",
            code=201
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=error_response(e.detail, e.status_code))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.post("/login")
def login(
    request: Request,
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        service = AuthService(db)
        result = service.authenticate_user(login_data)
        
        # Log activity
        client_host = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        log = ActivityLogCreate(
            action="login",
            description=f"User {login_data.username} logged in",
            ip_address=client_host,
            user_agent=user_agent
        )
        service.log_activity(result["user"].id, log)
        
        return success_response(
            data={
                "access_token": result["access_token"],
                "token_type": "bearer",
                "user": UserResponse.from_orm(result["user"])
            },
            message="Login successful"
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=error_response(e.detail, e.status_code))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.post("/logout")
def logout(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        service = AuthService(db)
        
        # Log activity
        client_host = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        log = ActivityLogCreate(
            action="logout",
            description=f"User {current_user.username} logged out",
            ip_address=client_host,
            user_agent=user_agent
        )
        service.log_activity(current_user.id, log)
        
        return success_response(
            message="Logout successful"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    return success_response(
        data=UserResponse.from_orm(current_user),
        message="User data retrieved successfully"
    )

@router.get("/activity-logs", response_model=dict)
def get_activity_logs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        service = AuthService(db)
        logs = service.get_activity_logs(skip, limit)
        return success_response(
            data=[ActivityLogResponse.from_orm(log) for log in logs],
            message="Activity logs retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/activity-logs/me")
def get_my_activity_logs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        service = AuthService(db)
        logs = service.get_user_activity_logs(current_user.id, skip, limit)
        return success_response(
            data=[ActivityLogResponse.from_orm(log) for log in logs],
            message="User activity logs retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )