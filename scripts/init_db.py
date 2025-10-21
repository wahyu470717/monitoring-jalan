import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import engine, Base
from app.domain.models import Jalan

def init_database():
    """Initialize database and create tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()