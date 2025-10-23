from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.dashboard_service import DashboardService
from app.api.schemas.response_schemas import success_response, error_response
from app.utils.auth import get_current_active_user
from app.domain.models import User

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get overall dashboard statistics"""
    try:
        service = DashboardService(db)
        stats = service.get_dashboard_stats()
        
        return success_response(
            data=stats,
            message="Dashboard statistics retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/pie-chart/kondisi")
def get_kondisi_pie_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get data for pie chart - Kondisi Jalan"""
    try:
        service = DashboardService(db)
        data = service.get_kondisi_distribution()
        
        return success_response(
            data=data,
            message="Kondisi distribution data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/pie-chart/status-penanganan")
def get_status_penanganan_pie_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get data for pie chart - Status Penanganan"""
    try:
        service = DashboardService(db)
        data = service.get_status_penanganan_distribution()
        
        return success_response(
            data=data,
            message="Status penanganan distribution data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/bar-chart/kecamatan")
def get_kecamatan_bar_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get data for bar chart - Jumlah Jalan per Kecamatan"""
    try:
        service = DashboardService(db)
        data = service.get_jalan_per_kecamatan()
        
        return success_response(
            data=data,
            message="Jalan per kecamatan data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/bar-chart/panjang-kecamatan")
def get_panjang_kecamatan_bar_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get data for bar chart - Total Panjang Jalan per Kecamatan"""
    try:
        service = DashboardService(db)
        data = service.get_panjang_per_kecamatan()
        
        return success_response(
            data=data,
            message="Panjang jalan per kecamatan data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/bar-chart/anggaran-kecamatan")
def get_anggaran_kecamatan_bar_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get data for bar chart - Total Anggaran per Kecamatan"""
    try:
        service = DashboardService(db)
        data = service.get_anggaran_per_kecamatan()
        
        return success_response(
            data=data,
            message="Anggaran per kecamatan data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/table/summary-kecamatan")
def get_summary_kecamatan_table(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get data for table - Summary per Kecamatan"""
    try:
        service = DashboardService(db)
        data = service.get_summary_per_kecamatan()
        
        return success_response(
            data=data,
            message="Summary per kecamatan retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/table/kondisi-detail")
def get_kondisi_detail_table(
    kondisi: str = None,
    kecamatan: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed table data with filters"""
    try:
        service = DashboardService(db)
        data = service.get_kondisi_detail(kondisi, kecamatan)
        
        return success_response(
            data=data,
            message="Kondisi detail data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )

@router.get("/line-chart/trend-tahunan")
def get_trend_tahunan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get data for line chart - Trend Pembangunan Tahunan"""
    try:
        service = DashboardService(db)
        data = service.get_trend_pembangunan_tahunan()
        
        return success_response(
            data=data,
            message="Trend pembangunan tahunan retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("Internal server error", 500)
        )