"""
Route: Simulator chat AI penipu
POST /api/v1/simulate/start    — Mulai sesi simulasi baru
POST /api/v1/simulate/message  — Kirim pesan dalam simulasi
"""

from fastapi import APIRouter, Request

from app.core.security import rate_limiter
from app.models.schemas import SimulateRequest, SimulateResponse, ScamCategory
from app.services.ai_agent import simulate_chat

router = APIRouter()


@router.post("/start", response_model=SimulateResponse)
async def start_simulation(request: Request, body: SimulateRequest):
    """
    Mulai sesi simulasi penipuan baru.
    User memilih skenario (phishing, investment scam, dll.)
    lalu mendapat pesan pembuka dari "penipu" AI.
    """
    rate_limiter.check(request)

    result = await simulate_chat(
        scenario=body.scenario,
        user_message="",
        session_id=None,  # Selalu buat sesi baru
    )
    return result


@router.post("/message", response_model=SimulateResponse)
async def send_message(request: Request, body: SimulateRequest):
    """
    Kirim pesan user dalam simulasi yang sedang berjalan.
    AI penipu akan merespons dan memberikan red-flags & tips.
    """
    rate_limiter.check(request)

    if not body.session_id:
        return SimulateResponse(
            session_id="",
            scammer_message="Error: session_id diperlukan. Mulai sesi baru terlebih dahulu.",
            red_flags=[],
            tip="",
            is_reveal=False,
        )

    result = await simulate_chat(
        scenario=body.scenario,
        user_message=body.user_message,
        session_id=body.session_id,
    )
    return result


@router.get("/scenarios")
async def list_scenarios():
    """Daftar skenario simulasi yang tersedia."""
    return {
        "scenarios": [
            {"id": ScamCategory.PHISHING, "name": "Phishing (Bank Palsu)", "icon": "🏦"},
            {"id": ScamCategory.INVESTMENT, "name": "Investasi Bodong", "icon": "📈"},
            {"id": ScamCategory.LOTTERY, "name": "Undian Berhadiah Palsu", "icon": "🎰"},
            {"id": ScamCategory.ROMANCE, "name": "Romance Scam", "icon": "💔"},
            {"id": ScamCategory.JOB_SCAM, "name": "Lowongan Kerja Palsu", "icon": "💼"},
        ]
    }
