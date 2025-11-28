import cv2
import torch
import numpy as np
import os
import ssl 
from gfpgan import GFPGANer
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from app.core.config import settings

# --- SSL HATASI ÇÖZÜMÜ ---
ssl._create_default_https_context = ssl._create_unverified_context

class AIEngine:
    def __init__(self):
        self.device = self._get_device()
        self.bg_upsampler = None
        self.face_restorer = None
        # Modelleri yükle
        self._load_models()

    def _get_device(self):
        if torch.backends.mps.is_available():
            print("✅ Güç Kaynağı: Apple M1 GPU (MPS)")
            return torch.device('mps')
        return torch.device('cpu')

    def _load_models(self):
        if not os.path.exists(settings.REALESRGAN_MODEL_PATH) or not os.path.exists(settings.GFPGAN_MODEL_PATH):
            print("❌ HATA: Model dosyaları yok!")
            return

        print("⚙️ AI Modelleri Yükleniyor (GOLD EDITION)...")
        
        # 1. Arka Plan Modeli (Real-ESRGAN)
        model_rrdb = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        
        self.bg_upsampler = RealESRGANer(
            scale=settings.UPSCALE_FACTOR,
            model_path=settings.REALESRGAN_MODEL_PATH,
            model=model_rrdb,
            tile=settings.TILE_SIZE,
            tile_pad=10,
            pre_pad=0,
            half=False,
            device=self.device
        )

        # 2. Yüz Modeli (GFPGAN) - Arka plana bağlıyoruz
        self.face_restorer = GFPGANer(
            model_path=settings.GFPGAN_MODEL_PATH,
            upscale=settings.UPSCALE_FACTOR,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=self.bg_upsampler
        )
        print("✅ AI Motoru Hazır!")

    def _mild_sharpen(self, img):
        """
        Karanlıklaştırmadan sadece hafif netlik veren filtre.
        (Senin beğendiğin o eski koddan aldım)
        """
        kernel = np.array([[0, -0.5, 0],
                           [-0.5, 3, -0.5],
                           [0, -0.5, 0]])
        return cv2.filter2D(img, -1, kernel)

    def process_image(self, input_path: str, output_path: str) -> bool:
        if self.face_restorer is None:
            return False

        # Resmi Oku
        img = cv2.imread(input_path, cv2.IMREAD_COLOR)
        if img is None:
            return False

        # Test optimizasyonu
        h, w = img.shape[:2]
        if w > 1000:
            scale = 500 / w
            img = cv2.resize(img, (0,0), fx=scale, fy=scale)

        try:
            # SİHİRLİ DOKUNUŞ (Entegre Mod)
            # weight=0.5 -> %50 Yapay Zeka, %50 Doğallık
            _, _, output = self.face_restorer.enhance(
                img, 
                has_aligned=False, 
                only_center_face=False, 
                paste_back=True, 
                weight=0.5 
            )
            
            if output is not None:
                # 1. Hafif Keskinlik Ver (Beğendiğin özellik)
                final_output = self._mild_sharpen(output)
                
                # 2. %100 Kalite ile Kaydet (Dosya boyutu yüksek olsun)
                cv2.imwrite(output_path, final_output, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                
                return True
            
        except Exception as e:
            print(f"❌ İşlem hatası: {e}")
            return False
            
        return False