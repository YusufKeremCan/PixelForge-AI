# 🚀 PixelForge AI

> **Next-Gen Full-Stack AI Restoration Engine.**
> Transforms low-quality images into 4K masterpieces using a hybrid **GFPGAN + Real-ESRGAN** pipeline.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Backend-FastAPI-green)
![Frontend](https://img.shields.io/badge/Frontend-Next.js_14-black)
![AI](https://img.shields.io/badge/AI-PyTorch_%2B_MPS-orange)

## 🌟 Features

- **Hybrid AI Pipeline:** Combines `Real-ESRGAN` (Background) and `GFPGAN` (Face Restoration) for seamless results.
- **Apple Silicon Optimized:** Fully optimized for **M1/M2/M3 chips** using Metal Performance Shaders (MPS).
- **Modern UI:** Built with **Next.js 14**, Tailwind CSS, and Framer Motion for smooth animations.
- **Privacy First:** Local processing. No cloud uploads. Your photos stay on your machine.
- **Smart Tiling:** Handles 4K resolution processing without crashing RAM.

## 🏗️ Architecture

| Component | Technology | Description |
|-----------|------------|-------------|
| **Backend** | FastAPI (Python) | High-performance async API server. |
| **AI Engine** | PyTorch | Deep Learning engine running GFPGAN & Real-ESRGAN. |
| **Frontend** | Next.js (React) | Modern, responsive, and animated user interface. |
| **Styling** | Tailwind CSS | Dark mode enabled sleek design. |

## 🚀 Installation

### 1. Clone the Repo
```bash
git clone [https://github.com/YusufKeremCan/PixelForge-AI.git](https://github.com/YusufKeremCan/PixelForge-AI.git)
cd PixelForge-AI