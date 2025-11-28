from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from app.core.config import settings
from app.services.engine import AIEngine

# Router (Yönlendirici) oluşturuyoruz
router = APIRouter()

# Yapay Zeka Motorunu Hazırla (Sadece bir kere yüklenir)
ai_engine = AIEngine()

@router.post("/enhance", summary="Fotoğrafı İyileştir")
async def enhance_image(file: UploadFile = File(...)):
    # 1. Dosya ismini güvenli hale getir
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    input_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    output_path = os.path.join(settings.RESULTS_DIR, unique_filename)

    # 2. Dosyayı kaydet
    try:
        with open(input_path, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya yükleme hatası: {e}")

    # 3. Motoru Çalıştır
    success = ai_engine.process_image(input_path, output_path)

    if success:
        # 4. Sonucu gönder
        return FileResponse(output_path, media_type="image/jpeg", filename=f"pixel_perfect_{unique_filename}")
    else:
        raise HTTPException(status_code=500, detail="Yapay zeka işlemi başarısız oldu.")