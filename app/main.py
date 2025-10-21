from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
from app.api.routes import jalan, dashboard
import os

# Create tables - PASTIKAN INI DIJALANKAN SEBELUM SEEDING
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistem Monitoring Infrastruktur Jalan",
    description="Dashboard untuk memonitoring kondisi infrastruktur jalan",
    version="1.0.0"
)

# Include routers
app.include_router(jalan.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Sistem Monitoring Infrastruktur Jalan API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)