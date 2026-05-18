"""
Route: Crowdsourced scam reports & database pencarian
POST   /api/v1/reports/         — Buat laporan baru
GET    /api/v1/reports/         — Daftar laporan (paginated)
GET    /api/v1/reports/search   — Cari nomor telepon/rekening
GET    /api/v1/reports/stats    — Statistik laporan
"""

from typing import Optional, List

from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import rate_limiter
from app.core.database import get_db
from app.models.schemas import ReportCreate, ReportResponse
from app.services.db_service import create_report, get_reports, search_number, get_report_stats

router = APIRouter()


@router.post("/", response_model=ReportResponse)
async def submit_report(
    request: Request,
    body: ReportCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Kirim laporan penipuan baru.
    Jika nomor telepon/rekening sudah ada, report_count akan bertambah.
    """
    rate_limiter.check(request)
    report = await create_report(db, body)
    return report


@router.get("/", response_model=List[ReportResponse])
async def list_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Daftar laporan penipuan dengan pagination & filter kategori."""
    reports = await get_reports(db, skip=skip, limit=limit, category=category)
    return reports


@router.get("/search")
async def search_reports(
    phone: Optional[str] = Query(None, description="Nomor telepon yang dicari"),
    account: Optional[str] = Query(None, description="Nomor rekening yang dicari"),
    db: AsyncSession = Depends(get_db),
):
    """
    Cek apakah nomor telepon/rekening pernah dilaporkan.
    Berguna untuk verifikasi sebelum bertransaksi.
    """
    if not phone and not account:
        return {"error": "Masukkan nomor telepon atau nomor rekening untuk dicari."}

    results = await search_number(db, phone=phone, account=account)
    return {
        "found": len(results) > 0,
        "count": len(results),
        "results": [ReportResponse.model_validate(r) for r in results],
        "message": f"Ditemukan {len(results)} laporan." if results else "Nomor tidak ditemukan dalam database laporan.",
    }


@router.get("/stats")
async def report_stats(db: AsyncSession = Depends(get_db)):
    """Statistik ringkasan seluruh laporan penipuan."""
    stats = await get_report_stats(db)
    return stats
