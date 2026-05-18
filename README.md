# 🛡️ AwasTipu — Deteksi Penipuan Online Berbasis AI

> **Lindungi dirimu dan orang-orang tercinta dari penipuan digital.**
> AwasTipu menggunakan kecerdasan buatan untuk mendeteksi, mengedukasi, dan melindungi masyarakat Indonesia dari modus penipuan online.

---

## 📋 Daftar Isi

- [Tentang Project](#-tentang-project)
- [Fitur Utama](#-fitur-utama)
- [Tech Stack](#-tech-stack)
- [Arsitektur](#-arsitektur)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Kontribusi](#-kontribusi)

---

## 🎯 Tentang Project

Penipuan online di Indonesia meningkat drastis setiap tahun. AwasTipu hadir sebagai solusi berbasis AI yang:

1. **Mendeteksi** pesan penipuan secara instan menggunakan analisis AI
2. **Mengedukasi** masyarakat melalui simulasi interaktif chat dengan "penipu" AI
3. **Melindungi** dengan database crowdsourced nomor penipu dari laporan masyarakat

---

## ✨ Fitur Utama

### 🔍 Fitur 1: Detektor Pesan & Vibe Meter
- Paste pesan SMS/WhatsApp/email untuk dianalisis AI
- Upload screenshot chat untuk OCR otomatis
- **Vibe Meter** — gauge visual menampilkan skor risiko (0-100)
- Detail taktik penipuan yang terdeteksi beserta penjelasan
- Rekomendasi tindakan yang harus dilakukan

### 🎮 Fitur 2: Simulator Penipuan (Playground)
- Chat interaktif dengan AI yang berperan sebagai penipu
- 5 skenario: Phishing, Investasi Bodong, Undian Palsu, Romance Scam, Lowongan Palsu
- UI mockup WhatsApp yang realistis
- Red flags ditandai real-time di setiap pesan penipu
- Reveal & edukasi di akhir simulasi

### 📋 Fitur 3: Database Laporan Masyarakat
- Cek nomor telepon/rekening sebelum bertransaksi
- Formulir laporan penipuan crowdsourced
- Daftar laporan dengan filter kategori
- Statistik penipuan nasional

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Frontend** | React 18 + TypeScript + Vite |
| **Styling** | Tailwind CSS 3.4 + Custom CSS Design System |
| **Backend** | Python FastAPI + Uvicorn |
| **AI/LLM** | Google Gemini 2.0 Flash via LangChain |
| **OCR** | Gemini Vision API + Tesseract (fallback) |
| **Database** | SQLite + SQLAlchemy (async) |
| **Testing** | Pytest + Httpx |

---

## 🏗️ Arsitektur

```
awastipu-root/
├── frontend/                  # React + Vite (TypeScript)
│   ├── public/                # Aset statis, index.html
│   └── src/
│       ├── assets/            # Gambar, icon
│       ├── components/
│       │   ├── ui/            # Button, Card, Badge, Input, Modal
│       │   └── shared/        # Navbar, Footer, Layout
│       ├── features/
│       │   ├── analyzer/      # Detektor Pesan & Vibe Meter
│       │   │   ├── components/  TextInput, VibeMeter, ResultCard
│       │   │   ├── hooks/       useAnalyzer
│       │   │   └── services/    analyzerService (API calls)
│       │   ├── simulator/     # Kamar Simulasi Penipuan
│       │   │   ├── components/  ChatRoom, ChatBubble, AlertBox, ScenarioSelector
│       │   │   └── hooks/       useSimulator
│       │   └── report/        # Database Laporan
│       │       └── components/  ReportForm, ReportList, NumberSearch
│       ├── pages/             # HomePage, AnalyzerPage, SimulatorPage, ReportPage
│       ├── styles/            # globals.css (Design System lengkap)
│       └── utils/             # helpers.ts (format, debounce, dll.)
│
├── backend/                   # FastAPI (Python)
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── analyze.py     # POST /text & /image
│   │   │   ├── simulate.py    # POST /start & /message, GET /scenarios
│   │   │   └── reports.py     # CRUD laporan + search
│   │   ├── core/
│   │   │   ├── config.py      # Settings dari .env
│   │   │   ├── database.py    # Async SQLAlchemy engine
│   │   │   └── security.py    # Rate limiter, sanitizer
│   │   ├── services/
│   │   │   ├── ai_agent.py    # Gemini AI + rule-based fallback
│   │   │   ├── vision.py      # OCR (Gemini Vision + Tesseract)
│   │   │   └── db_service.py  # Database queries
│   │   └── models/
│   │       └── schemas.py     # ORM models + Pydantic schemas
│   ├── tests/
│   │   └── test_api.py        # Unit tests
│   ├── requirements.txt
│   └── main.py                # FastAPI entry point
│
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** ≥ 18
- **Python** ≥ 3.10
- **Google Gemini API Key** (opsional, ada fallback rule-based)

### 1. Clone & Setup

```bash
git clone https://github.com/your-username/awastipu-root.git
cd awastipu-root
```

### 2. Backend

```bash
cd backend

# Buat virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy & edit environment
copy .env.example .env
# Edit .env → masukkan GEMINI_API_KEY

# Jalankan server
uvicorn main:app --reload --port 8000
```

Backend berjalan di `http://localhost:8000`
Dokumentasi API: `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Jalankan dev server
npm run dev
```

Frontend berjalan di `http://localhost:5173`

---

## 📡 API Documentation

### Analyze

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/v1/analyze/text` | Analisis teks pesan |
| POST | `/api/v1/analyze/image` | Upload & analisis screenshot |

### Simulator

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/v1/simulate/start` | Mulai sesi simulasi |
| POST | `/api/v1/simulate/message` | Kirim pesan dalam simulasi |
| GET | `/api/v1/simulate/scenarios` | Daftar skenario tersedia |

### Reports

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/v1/reports/` | Kirim laporan baru |
| GET | `/api/v1/reports/` | Daftar laporan (paginated) |
| GET | `/api/v1/reports/search` | Cari nomor telepon/rekening |
| GET | `/api/v1/reports/stats` | Statistik laporan |

---

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch fitur: `git checkout -b fitur-baru`
3. Commit perubahan: `git commit -m "Tambah fitur X"`
4. Push ke branch: `git push origin fitur-baru`
5. Buat Pull Request

---

## 📄 Lisensi

Project ini dibuat untuk **Juara Vibe Coding 2026** 🇮🇩

---

<p align="center">
  <b>🛡️ AwasTipu — Karena mencegah lebih baik daripada menjadi korban.</b>
</p>
