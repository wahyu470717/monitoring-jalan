from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.models import Jalan
from typing import List, Dict, Optional

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_stats(self) -> Dict:
        """Get overall statistics for dashboard"""
        total_jalan = self.db.query(Jalan).filter(Jalan.is_active == True).count()
        
        total_panjang = self.db.query(
            func.sum(Jalan.panjang)
        ).filter(Jalan.is_active == True).scalar() or 0
        
        total_anggaran = self.db.query(
            func.sum(Jalan.anggaran)
        ).filter(Jalan.is_active == True).scalar() or 0
        
        kondisi_stats = self.db.query(
            Jalan.kondisi,
            func.count(Jalan.id)
        ).filter(Jalan.is_active == True).group_by(Jalan.kondisi).all()
        
        status_stats = self.db.query(
            Jalan.status_penanganan,
            func.count(Jalan.id)
        ).filter(Jalan.is_active == True).group_by(Jalan.status_penanganan).all()
        
        kondisi_dict = {kondisi: count for kondisi, count in kondisi_stats}
        status_dict = {status: count for status, count in status_stats}
        
        return {
            "total_jalan": total_jalan,
            "total_panjang": round(total_panjang, 2),
            "total_anggaran": round(total_anggaran, 2),
            "kondisi_baik": kondisi_dict.get("Baik", 0),
            "kondisi_sedang": kondisi_dict.get("Sedang", 0),
            "kondisi_rusak": kondisi_dict.get("Rusak", 0),
            "kondisi_rusak_berat": kondisi_dict.get("Rusak Berat", 0),
            "status_belum": status_dict.get("Belum", 0),
            "status_proses": status_dict.get("Proses", 0),
            "status_selesai": status_dict.get("Selesai", 0)
        }
    
    def get_kondisi_distribution(self) -> List[Dict]:
        """Get data for pie chart - distribution by kondisi"""
        results = self.db.query(
            Jalan.kondisi,
            func.count(Jalan.id).label('count'),
            func.sum(Jalan.panjang).label('total_panjang')
        ).filter(Jalan.is_active == True).group_by(Jalan.kondisi).all()
        
        return [
            {
                "label": row.kondisi,
                "value": row.count,
                "total_panjang": round(row.total_panjang or 0, 2)
            }
            for row in results
        ]
    
    def get_status_penanganan_distribution(self) -> List[Dict]:
        """Get data for pie chart - distribution by status penanganan"""
        results = self.db.query(
            Jalan.status_penanganan,
            func.count(Jalan.id).label('count')
        ).filter(Jalan.is_active == True).group_by(Jalan.status_penanganan).all()
        
        return [
            {
                "label": row.status_penanganan,
                "value": row.count
            }
            for row in results
        ]
    
    def get_jalan_per_kecamatan(self) -> List[Dict]:
        """Get data for bar chart - jumlah jalan per kecamatan"""
        results = self.db.query(
            Jalan.kecamatan,
            func.count(Jalan.id).label('jumlah')
        ).filter(Jalan.is_active == True).group_by(
            Jalan.kecamatan
        ).order_by(func.count(Jalan.id).desc()).all()
        
        return [
            {
                "kecamatan": row.kecamatan,
                "jumlah": row.jumlah
            }
            for row in results
        ]
    
    def get_panjang_per_kecamatan(self) -> List[Dict]:
        """Get data for bar chart - total panjang jalan per kecamatan"""
        results = self.db.query(
            Jalan.kecamatan,
            func.sum(Jalan.panjang).label('total_panjang')
        ).filter(Jalan.is_active == True).group_by(
            Jalan.kecamatan
        ).order_by(func.sum(Jalan.panjang).desc()).all()
        
        return [
            {
                "kecamatan": row.kecamatan,
                "total_panjang": round(row.total_panjang or 0, 2)
            }
            for row in results
        ]
    
    def get_anggaran_per_kecamatan(self) -> List[Dict]:
        """Get data for bar chart - total anggaran per kecamatan"""
        results = self.db.query(
            Jalan.kecamatan,
            func.sum(Jalan.anggaran).label('total_anggaran')
        ).filter(Jalan.is_active == True).group_by(
            Jalan.kecamatan
        ).order_by(func.sum(Jalan.anggaran).desc()).all()
        
        return [
            {
                "kecamatan": row.kecamatan,
                "total_anggaran": round(row.total_anggaran or 0, 2)
            }
            for row in results
        ]
    
    def get_summary_per_kecamatan(self) -> List[Dict]:
        """Get summary table data per kecamatan"""
        results = self.db.query(
            Jalan.kecamatan,
            func.count(Jalan.id).label('jumlah_jalan'),
            func.sum(Jalan.panjang).label('total_panjang'),
            func.sum(Jalan.anggaran).label('total_anggaran'),
            func.sum(func.case((Jalan.kondisi == 'Baik', 1), else_=0)).label('baik'),
            func.sum(func.case((Jalan.kondisi == 'Sedang', 1), else_=0)).label('sedang'),
            func.sum(func.case((Jalan.kondisi == 'Rusak', 1), else_=0)).label('rusak'),
            func.sum(func.case((Jalan.kondisi == 'Rusak Berat', 1), else_=0)).label('rusak_berat')
        ).filter(Jalan.is_active == True).group_by(Jalan.kecamatan).all()
        
        return [
            {
                "kecamatan": row.kecamatan,
                "jumlah_jalan": row.jumlah_jalan,
                "total_panjang": round(row.total_panjang or 0, 2),
                "total_anggaran": round(row.total_anggaran or 0, 2),
                "kondisi": {
                    "baik": row.baik,
                    "sedang": row.sedang,
                    "rusak": row.rusak,
                    "rusak_berat": row.rusak_berat
                }
            }
            for row in results
        ]
    
    def get_kondisi_detail(
        self, 
        kondisi: Optional[str] = None, 
        kecamatan: Optional[str] = None
    ) -> List[Dict]:
        """Get detailed data with optional filters"""
        query = self.db.query(Jalan).filter(Jalan.is_active == True)
        
        if kondisi:
            query = query.filter(Jalan.kondisi == kondisi)
        if kecamatan:
            query = query.filter(Jalan.kecamatan == kecamatan)
        
        results = query.all()
        
        return [
            {
                "id": row.id,
                "nama_jalan": row.nama_jalan,
                "kecamatan": row.kecamatan,
                "kelurahan": row.kelurahan,
                "panjang": round(row.panjang, 2),
                "lebar": round(row.lebar, 2),
                "kondisi": row.kondisi,
                "jenis_perkerasan": row.jenis_perkerasan,
                "status_penanganan": row.status_penanganan,
                "anggaran": round(row.anggaran or 0, 2),
                "tahun_pembangunan": row.tahun_pembangunan
            }
            for row in results
        ]
    
    def get_trend_pembangunan_tahunan(self) -> List[Dict]:
        """Get yearly trend data for line chart"""
        results = self.db.query(
            Jalan.tahun_pembangunan,
            func.count(Jalan.id).label('jumlah'),
            func.sum(Jalan.panjang).label('total_panjang'),
            func.sum(Jalan.anggaran).label('total_anggaran')
        ).filter(
            Jalan.is_active == True,
            Jalan.tahun_pembangunan.isnot(None)
        ).group_by(
            Jalan.tahun_pembangunan
        ).order_by(Jalan.tahun_pembangunan).all()
        
        return [
            {
                "tahun": row.tahun_pembangunan,
                "jumlah": row.jumlah,
                "total_panjang": round(row.total_panjang or 0, 2),
                "total_anggaran": round(row.total_anggaran or 0, 2)
            }
            for row in results
        ]