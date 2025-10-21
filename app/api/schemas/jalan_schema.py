from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JalanBase(BaseModel):
    nama_jalan: str
    panjang: float
    lebar: float
    kondisi: str
    jenis_perkerasan: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    kecamatan: str
    kelurahan: str
    tahun_pembangunan: Optional[int] = None
    anggaran: Optional[float] = None
    status_penanganan: str
    deskripsi: Optional[str] = None
    foto_path: Optional[str] = None

class JalanCreate(JalanBase):
    pass

class JalanUpdate(JalanBase):
    pass

class Jalan(JalanBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_jalan: int
    total_panjang: float
    kondisi_baik: int
    kondisi_sedang: int
    kondisi_rusak: int
    kondisi_rusak_berat: int
    total_anggaran: float