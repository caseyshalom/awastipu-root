"""
Database Service — Query laporan penipuan & pattern matching.
"""

from typing import Optional, List

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import ScamReport
from app.models.schemas import ReportCreate, ReportResponse


async def create_report(db: AsyncSession, report_data: ReportCreate) -> ScamReport:
    """Buat laporan penipuan baru."""
    # Cek apakah nomor telepon/rekening sudah pernah dilaporkan
    existing = None
    if report_data.phone_number:
        existing = await db.execute(
            select(ScamReport).where(ScamReport.phone_number == report_data.phone_number)
        )
        existing = existing.scalar_one_or_none()
    elif report_data.bank_account:
        existing = await db.execute(
            select(ScamReport).where(ScamReport.bank_account == report_data.bank_account)
        )
        existing = existing.scalar_one_or_none()

    if existing:
        # Update report count jika sudah ada
        existing.report_count += 1
        existing.risk_score = min(100.0, existing.risk_score + 10.0)
        existing.description += f"\n---\n{report_data.description}"
        await db.flush()
        return existing

    # Buat laporan baru
    new_report = ScamReport(
        phone_number=report_data.phone_number,
        bank_account=report_data.bank_account,
        scam_category=report_data.scam_category.value,
        description=report_data.description,
        evidence_url=report_data.evidence_url,
        reporter_alias=report_data.reporter_alias,
        risk_score=25.0,  # Skor awal
    )
    db.add(new_report)
    await db.flush()
    return new_report


async def get_reports(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
) -> List[ScamReport]:
    """Ambil daftar laporan penipuan dengan pagination."""
    query = select(ScamReport).order_by(ScamReport.created_at.desc())

    if category:
        query = query.where(ScamReport.scam_category == category)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def search_number(
    db: AsyncSession,
    phone: Optional[str] = None,
    account: Optional[str] = None,
) -> List[ScamReport]:
    """Cari nomor telepon atau rekening dalam database laporan."""
    conditions = []
    if phone:
        conditions.append(ScamReport.phone_number.contains(phone))
    if account:
        conditions.append(ScamReport.bank_account.contains(account))

    if not conditions:
        return []

    query = select(ScamReport).where(or_(*conditions))
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_report_stats(db: AsyncSession) -> dict:
    """Statistik ringkasan laporan."""
    total = await db.execute(select(func.count(ScamReport.id)))
    total_count = total.scalar() or 0

    by_category = await db.execute(
        select(ScamReport.scam_category, func.count(ScamReport.id))
        .group_by(ScamReport.scam_category)
    )

    categories = {row[0]: row[1] for row in by_category.all()}

    return {
        "total_reports": total_count,
        "by_category": categories,
    }
