import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.domain.models import Jalan
import random

def create_sample_data():
    # PASTIKAN TABEL DIBUAT TERLEBIH DAHULU
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Jangan gunakan delete all, gunakan approach yang lebih aman
        # Cek apakah ada data existing
        existing_count = db.query(Jalan).count()
        if existing_count > 0:
            print(f"Database sudah berisi {existing_count} data. Menambahkan data baru...")
        else:
            print("Database kosong. Menambahkan data sample...")
        
        # Sample data
        jalan_data = [
            {
                "nama_jalan": "Jalan Merdeka",
                "panjang": 2500,
                "lebar": 12,
                "kondisi": "Baik",
                "jenis_perkerasan": "Aspal",
                "latitude": -6.2088,
                "longitude": 106.8456,
                "kecamatan": "Gambir",
                "kelurahan": "Gambir",
                "tahun_pembangunan": 2020,
                "anggaran": 2500,
                "status_penanganan": "Selesai",
                "deskripsi": "Jalan utama di pusat kota"
            },
            {
                "nama_jalan": "Jalan Sudirman",
                "panjang": 3500,
                "lebar": 15,
                "kondisi": "Sedang",
                "jenis_perkerasan": "Aspal",
                "latitude": -6.2088,
                "longitude": 106.8456,
                "kecamatan": "Tanah Abang",
                "kelurahan": "Bendungan Hilir",
                "tahun_pembangunan": 2018,
                "anggaran": 3500,
                "status_penanganan": "Proses",
                "deskripsi": "Jalan protokol dengan aktivitas tinggi"
            },
            {
                "nama_jalan": "Jalan Thamrin",
                "panjang": 2000,
                "lebar": 10,
                "kondisi": "Rusak",
                "jenis_perkerasan": "Aspal",
                "latitude": -6.2088,
                "longitude": 106.8456,
                "kecamatan": "Menteng",
                "kelurahan": "Menteng",
                "tahun_pembangunan": 2015,
                "anggaran": 1800,
                "status_penanganan": "Belum",
                "deskripsi": "Perlu perbaikan segera"
            },
            {
                "nama_jalan": "Jalan Gatot Subroto",
                "panjang": 5000,
                "lebar": 20,
                "kondisi": "Baik",
                "jenis_perkerasan": "Beton",
                "latitude": -6.2088,
                "longitude": 106.8456,
                "kecamatan": "Kuningan",
                "kelurahan": "Kuningan",
                "tahun_pembangunan": 2021,
                "anggaran": 5000,
                "status_penanganan": "Selesai",
                "deskripsi": "Jalan tol dalam kota"
            },
            {
                "nama_jalan": "Jalan Pasar Minggu",
                "panjang": 1500,
                "lebar": 8,
                "kondisi": "Rusak Berat",
                "jenis_perkerasan": "Aspal",
                "latitude": -6.2088,
                "longitude": 106.8456,
                "kecamatan": "Pasar Minggu",
                "kelurahan": "Pasar Minggu",
                "tahun_pembangunan": 2010,
                "anggaran": 1200,
                "status_penanganan": "Belum",
                "deskripsi": "Perlu rekonstruksi total"
            }
        ]

        # Add more sample data
        kecamatan_list = ["Gambir", "Tanah Abang", "Menteng", "Kuningan", "Pasar Minggu", "Tebet", "Setiabudi"]
        kondisi_list = ["Baik", "Sedang", "Rusak", "Rusak Berat"]
        status_list = ["Belum", "Proses", "Selesai"]
        
        for i in range(15):
            jalan_data.append({
                "nama_jalan": f"Jalan Contoh {i+1}",
                "panjang": random.randint(500, 3000),
                "lebar": random.randint(6, 15),
                "kondisi": random.choice(kondisi_list),
                "jenis_perkerasan": "Aspal",
                "latitude": -6.2088 + random.uniform(-0.1, 0.1),
                "longitude": 106.8456 + random.uniform(-0.1, 0.1),
                "kecamatan": random.choice(kecamatan_list),
                "kelurahan": f"Kelurahan {random.randint(1, 10)}",
                "tahun_pembangunan": random.randint(2010, 2023),
                "anggaran": random.randint(800, 3000),
                "status_penanganan": random.choice(status_list),
                "deskripsi": f"Jalan sample untuk testing {i+1}"
            })

        # Insert data - hanya insert jika belum ada
        for data in jalan_data:
            # Cek apakah data sudah ada berdasarkan nama jalan
            existing = db.query(Jalan).filter(Jalan.nama_jalan == data["nama_jalan"]).first()
            if not existing:
                jalan = Jalan(**data)
                db.add(jalan)
        
        db.commit()
        print("Sample data berhasil ditambahkan!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()