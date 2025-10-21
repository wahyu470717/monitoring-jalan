from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Jalan(Base):
    __tablename__ = "jalan"
    
    id = Column(Integer, primary_key=True, index=True)
    nama_jalan = Column(String(255), nullable=False)
    panjang = Column(Float, nullable=False)  # dalam meter
    lebar = Column(Float, nullable=False)    # dalam meter
    kondisi = Column(String(50), nullable=False)  # Baik, Sedang, Rusak, Rusak Berat
    jenis_perkerasan = Column(String(100), nullable=False)  # Aspal, Beton, Tanah
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    kecamatan = Column(String(100), nullable=False)
    kelurahan = Column(String(100), nullable=False)
    tahun_pembangunan = Column(Integer, nullable=True)
    anggaran = Column(Float, nullable=True)  # dalam juta rupiah
    status_penanganan = Column(String(50), nullable=False)  # Belum, Proses, Selesai
    deskripsi = Column(Text, nullable=True)
    foto_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)