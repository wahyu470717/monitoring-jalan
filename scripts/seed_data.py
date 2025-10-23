import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.domain.models import Jalan, User
from app.utils.auth import get_password_hash
import random

# Create tables
Base.metadata.create_all(bind=engine)

# def create_admin_user(db):
#     """Create default admin user"""
#     admin = db.query(User).filter(User.username == "admin").first()
#     if not admin:
#         admin = User(
#             username="admin",
#             email="admin@monitoring-jalan.com",
#             full_name="Administrator",
#             hashed_password=get_password_hash("admin123"),
#             is_active=True,
#             is_superuser=True
#         )
#         db.add(admin)
#         db.commit()
#         print("✓ Admin user created (username: admin, password: admin123)")
#     else:
#         print("✓ Admin user already exists")

from app.utils.auth import get_password_hash

def create_admin_user(db):
    """Create default admin user"""
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        # Gunakan password yang lebih sederhana
        admin_password = "admin123"
        
        admin = User(
            username="admin",
            email="admin@monitoring-jalan.com",
            full_name="Administrator",
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            is_superuser=True
        )
        db.add(admin)
        db.commit()
        print(f"✓ Admin user created (username: admin, password: {admin_password})")
    else:
        print("✓ Admin user already exists")
        
def create_sample_jalan_data(db):
    """Create sample jalan data"""
    existing_count = db.query(Jalan).count()
    if existing_count > 0:
        print(f"✓ {existing_count} jalan records already exist")
        return
    
    kecamatan_list = [
        "Bandung Wetan", "Bandung Kulon", "Bojongloa Kaler", 
        "Bojongloa Kidul", "Astana Anyar", "Regol", "Lengkong", 
        "Batununggal", "Sumur Bandung", "Andir"
    ]
    
    kelurahan_dict = {
        "Bandung Wetan": ["Citarum", "Tamansari", "Cihapit"],
        "Bandung Kulon": ["Cijerah", "Gempolsari", "Warung Muncang"],
        "Bojongloa Kaler": ["Babakan Asih", "Babakan Tarogong", "Jamika"],
        "Bojongloa Kidul": ["Cibaduyut", "Kebon Lega", "Mekarwangi"],
        "Astana Anyar": ["Karasak", "Pelindung Hewan", "Karanganyar"],
        "Regol": ["Cigereleng", "Pungkur", "Ancol"],
        "Lengkong": ["Cikawao", "Lingkar Selatan", "Paledang"],
        "Batununggal": ["Binong", "Kujangsari", "Gumuruh"],
        "Sumur Bandung": ["Braga", "Kebon Pisang", "Merdeka"],
        "Andir": ["Campaka", "Dunguscariang", "Maleber"]
    }
    
    nama_jalan_prefix = [
        "Jl. Raya", "Jl. Utama", "Jl. Protokol", "Jl. Veteran",
        "Jl. Sudirman", "Jl. Ahmad Yani", "Jl. Gatot Subroto",
        "Jl. Dipatiukur", "Jl. Soekarno Hatta", "Jl. Cihampelas"
    ]
    
    kondisi_list = ["Baik", "Sedang", "Rusak", "Rusak Berat"]
    jenis_perkerasan_list = ["Aspal", "Beton", "Paving Block", "Tanah"]
    status_penanganan_list = ["Belum", "Proses", "Selesai"]
    
    sample_data = []
    
    for kecamatan in kecamatan_list:
        kelurahan_list = kelurahan_dict.get(kecamatan, ["Kelurahan 1", "Kelurahan 2"])
        
        # Generate 5-10 roads per kecamatan
        num_roads = random.randint(5, 10)
        
        for i in range(num_roads):
            kelurahan = random.choice(kelurahan_list)
            nama_prefix = random.choice(nama_jalan_prefix)
            nama_jalan = f"{nama_prefix} {kelurahan} {i+1}"
            
            kondisi = random.choice(kondisi_list)
            
            # Generate realistic data based on kondisi
            if kondisi == "Baik":
                panjang = random.uniform(500, 3000)
                lebar = random.uniform(6, 12)
                anggaran = random.uniform(50, 200)
                status = "Selesai"
            elif kondisi == "Sedang":
                panjang = random.uniform(400, 2500)
                lebar = random.uniform(5, 10)
                anggaran = random.uniform(100, 400)
                status = random.choice(["Proses", "Belum"])
            elif kondisi == "Rusak":
                panjang = random.uniform(300, 2000)
                lebar = random.uniform(4, 8)
                anggaran = random.uniform(200, 600)
                status = random.choice(["Belum", "Proses"])
            else:  # Rusak Berat
                panjang = random.uniform(200, 1500)
                lebar = random.uniform(3, 7)
                anggaran = random.uniform(400, 1000)
                status = "Belum"
            
            jalan = Jalan(
                nama_jalan=nama_jalan,
                panjang=round(panjang, 2),
                lebar=round(lebar, 2),
                kondisi=kondisi,
                jenis_perkerasan=random.choice(jenis_perkerasan_list),
                latitude=random.uniform(-6.95, -6.88),
                longitude=random.uniform(107.57, 107.68),
                kecamatan=kecamatan,
                kelurahan=kelurahan,
                tahun_pembangunan=random.randint(2010, 2024),
                anggaran=round(anggaran, 2),
                status_penanganan=status,
                deskripsi=f"Jalan {nama_jalan} di {kelurahan}, Kecamatan {kecamatan}",
                is_active=True
            )
            sample_data.append(jalan)
    
    # Bulk insert
    db.bulk_save_objects(sample_data)
    db.commit()
    print(f"✓ Created {len(sample_data)} sample jalan records")

def main():
    db = SessionLocal()
    try:
        print("Starting database seeding...")
        print("-" * 50)
        
        create_admin_user(db)
        create_sample_jalan_data(db)
        
        print("-" * 50)
        print("✓ Database seeding completed successfully!")
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        
    except Exception as e:
        print(f"✗ Error during seeding: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()