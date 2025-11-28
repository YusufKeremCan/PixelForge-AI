'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Sparkles, Zap, Download, RefreshCw } from 'lucide-react';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResultImage(null); // Yeni dosya seçince eski sonucu temizle
    }
  };

  const handleEnhance = async () => {
    if (!file) return;
    setIsProcessing(true);

    try {
      // 1. Form verisi oluştur
      const formData = new FormData();
      formData.append('file', file);

      // 2. Backend'e gönder (API Çağrısı)
      const response = await fetch('http://127.0.0.1:8000/api/v1/enhance', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('İşlem başarısız oldu');

      // 3. Gelen sonucu al (Blob olarak)
      const blob = await response.blob();
      const downloadUrl = URL.createObjectURL(blob);
      setResultImage(downloadUrl);
      
    } catch (error) {
      alert("Bir hata oluştu kanka! Backend açık mı?");
      console.error(error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white selection:bg-purple-500 selection:text-white">
      {/* NAVİGASYON */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/10 bg-black/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Zap className="w-6 h-6 text-purple-500 fill-purple-500" />
            <span className="font-bold text-xl tracking-tighter">ProjectPixel</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/20">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              <span className="text-xs font-medium text-green-400">Sistem Online</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-32 pb-20 px-6 max-w-6xl mx-auto flex flex-col items-center text-center">
        
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent">
            Fotoğraflarını <br /> <span className="text-purple-500">Yapay Zeka</span> ile Canlandır.
          </h1>
        </motion.div>

        {/* --- ÇALIŞMA ALANI --- */}
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2 }} className="w-full mt-10">
          
          {!preview ? (
            // BOŞ DURUM (Yükleme Ekranı)
            <div className="max-w-xl mx-auto">
              <div className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
                <label className="relative flex flex-col items-center justify-center gap-4 cursor-pointer h-64 bg-zinc-900 border border-white/10 rounded-xl hover:bg-zinc-800 transition-all">
                  <div className="p-4 bg-purple-500/10 rounded-full text-purple-400">
                    <Upload className="w-8 h-8" />
                  </div>
                  <div className="space-y-1">
                    <p className="font-medium">Fotoğrafı buraya bırak</p>
                    <p className="text-xs text-gray-500">JPG, PNG (Max 10MB)</p>
                  </div>
                  <input type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                </label>
              </div>
            </div>
          ) : (
            // DOLU DURUM (Sonuç Ekranı)
            <div className="grid md:grid-cols-2 gap-8 items-start">
              
              {/* SOL: Orijinal */}
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider">Orijinal</h3>
                <div className="relative rounded-xl overflow-hidden border border-white/20 aspect-[4/3] bg-black/50 group">
                  <img src={preview} alt="Orijinal" className="w-full h-full object-contain" />
                </div>
              </div>

              {/* SAĞ: Sonuç (Veya Yükleniyor) */}
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-purple-400 uppercase tracking-wider">AI Restore Edilmiş</h3>
                <div className="relative rounded-xl overflow-hidden border border-purple-500/30 aspect-[4/3] bg-black/50 flex items-center justify-center">
                  
                  {resultImage ? (
                    <img src={resultImage} alt="Sonuç" className="w-full h-full object-contain" />
                  ) : (
                    <div className="flex flex-col items-center gap-4 text-gray-500">
                      {isProcessing ? (
                        <>
                          <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                          <p className="text-sm animate-pulse text-purple-300">Pikseller işleniyor...</p>
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-10 h-10 opacity-20" />
                          <p className="text-sm">Sonuç burada görünecek</p>
                        </>
                      )}
                    </div>
                  )}
                </div>

                {/* Butonlar */}
                <div className="flex gap-3 pt-2">
                  {!resultImage ? (
                    <button 
                      onClick={handleEnhance} 
                      disabled={isProcessing}
                      className="w-full py-4 rounded-xl font-bold text-white bg-purple-600 hover:bg-purple-500 transition-all shadow-lg shadow-purple-900/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {isProcessing ? "Lütfen Bekle..." : "Sihirli Dokunuş Yap ✨"}
                    </button>
                  ) : (
                    <>
                      <button 
                        onClick={() => { setFile(null); setPreview(null); setResultImage(null); }}
                        className="flex-1 py-4 rounded-xl font-medium text-gray-300 bg-white/5 hover:bg-white/10 transition-colors flex items-center justify-center gap-2"
                      >
                        <RefreshCw className="w-4 h-4" /> Yeni Fotoğraf
                      </button>
                      <a 
                        href={resultImage} 
                        download="projectpixel-hd.jpg"
                        className="flex-[2] py-4 rounded-xl font-bold text-black bg-white hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
                      >
                        <Download className="w-4 h-4" /> İndir (HD)
                      </a>
                    </>
                  )}
                </div>
              </div>

            </div>
          )}

        </motion.div>
      </main>
    </div>
  );
}