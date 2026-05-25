"""
AwasTipu — Backend Entry Point
FastAPI application server untuk deteksi penipuan berbasis AI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.v1.analyze import router as analyze_router
from app.api.v1.simulate import router as simulate_router
from app.api.v1.emergency import router as emergency_router
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(
    title="AwasTipu API",
    description="API Backend untuk deteksi & edukasi penipuan online berbasis AI",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
async def on_startup():
    await init_db()

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Router Registration ──
app.include_router(analyze_router,  prefix="/api/v1/analyze",  tags=["Analyzer"])
app.include_router(simulate_router, prefix="/api/v1/simulate", tags=["Simulator"])
app.include_router(emergency_router,  prefix="/api/v1/emergency",  tags=["Emergency Guide"])


@app.get("/api/health", tags=["Health"])
async def health_check():
    """API health-check endpoint."""
    return {
        "status": "ok",
        "service": "awastipu-api",
        "version": "0.1.0",
    }

# ── SPA Serving (React Frontend) ──
# Lokasi folder statis yang dicopy saat proses Docker build
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Buat folder dummy untuk berjaga-jaga jika dijalankan lokal sebelum build frontend
os.makedirs(STATIC_DIR, exist_ok=True)
index_file = os.path.join(STATIC_DIR, "index.html")
if not os.path.exists(index_file):
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("<h1>AwasTipu Frontend Belum Di-build</h1><p>Jalankan 'npm run build' di folder frontend terlebih dahulu.</p>")

# Mount folder assets (CSS, JS) yang digenerate oleh Vite
assets_dir = os.path.join(STATIC_DIR, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Catch-all route untuk menangani sistem navigasi React Router (SPA)
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react_app(full_path: str):
    # Jika me-request file spesifik di root (seperti favicon.ico, logo.png)
    requested_file = os.path.join(STATIC_DIR, full_path)
    if os.path.isfile(requested_file):
        return FileResponse(requested_file)
    
    # Jika rute tidak ditemukan (misal: /simulator, /report), selalu kembalikan index.html
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
