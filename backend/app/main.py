from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- YENİ
from app.core.config import settings
from app.api import routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Yusuf Kerem'in Profesyonel AI Restorasyon API'si"
)

# --- GÜMRÜK İZİNLERİ (CORS) ---
# Frontend (localhost:3000) Backend'e erişebilsin diye izin veriyoruz.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için normalde "http://localhost:3000" yazılır ama şimdilik herkese açalım
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api/v1", tags=["AI Restoration"])

@app.get("/", tags=["Status"])
def read_root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "🟢 Sistem Aktif ve Hazır"
    }