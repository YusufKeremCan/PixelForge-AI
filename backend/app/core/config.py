import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Proje Bilgileri
    PROJECT_NAME: str = "Project Pixel API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Klasör Ayarları (Otomatik algılar)
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    WEIGHTS_DIR: str = os.path.join(BASE_DIR, "weights")
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    RESULTS_DIR: str = os.path.join(BASE_DIR, "results")

    # Model Dosya Yolları (Merkezi Yönetim)
    REALESRGAN_MODEL_PATH: str = os.path.join(WEIGHTS_DIR, "RealESRGAN_x4plus.pth")
    GFPGAN_MODEL_PATH: str = os.path.join(WEIGHTS_DIR, "GFPGANv1.3.pth")
    
    # Model Ayarları
    TILE_SIZE: int = 400  # M1 RAM Koruması
    UPSCALE_FACTOR: int = 4

    class Config:
        case_sensitive = True

# Ayarları dışarıya açıyoruz
settings = Settings()

# Klasörler yoksa oluştur (Otomatik kurulum)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RESULTS_DIR, exist_ok=True)