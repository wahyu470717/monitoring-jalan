from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    activity_logs = relationship("ActivityLog", back_populates="user")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # login, logout, create, update, delete
    entity_type = Column(String(50), nullable=True)  # jalan, user, etc
    entity_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="activity_logs")

class Jalan(Base):
    __tablename__ = "jalan"
    
    id = Column(Integer, primary_key=True, index=True)
    nama_jalan = Column(String(255), nullable=False, index=True)
    panjang = Column(Float, nullable=False)  # dalam meter
    lebar = Column(Float, nullable=False)    # dalam meter
    kondisi = Column(String(50), nullable=False, index=True)  # Baik, Sedang, Rusak, Rusak Berat
    jenis_perkerasan = Column(String(100), nullable=False)  # Aspal, Beton, Tanah
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    kecamatan = Column(String(100), nullable=False, index=True)
    kelurahan = Column(String(100), nullable=False)
    tahun_pembangunan = Column(Integer, nullable=True)
    anggaran = Column(Float, nullable=True)  # dalam juta rupiah
    status_penanganan = Column(String(50), nullable=False)  # Belum, Proses, Selesai
    deskripsi = Column(Text, nullable=True)
    foto_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)