"""
Pydantic schemas — request & response models untuk semua endpoint.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


# ════════════════════════════════════════════════════════════════════════════
# ENUMS
# ════════════════════════════════════════════════════════════════════════════

class RiskLevel(str, Enum):
    AMAN    = "AMAN"
    WASPADA = "WASPADA"
    BAHAYA  = "BAHAYA"


class ScamModus(str, Enum):
    KURIR_APK          = "KURIR_APK"
    UNDANGAN_APK       = "UNDANGAN_APK"
    TEBAK_BERHADIAH    = "TEBAK_BERHADIAH"
    CS_BANK_PALSU      = "CS_BANK_PALSU"


class ScamCategory(str, Enum):
    PHISHING = "phishing"
    INVESTMENT = "investment_scam"
    LOTTERY = "lottery_scam"
    ROMANCE = "romance_scam"
    JOB_SCAM = "job_scam"
    IMPERSONATION = "impersonation"
    SHOPPING_SCAM = "shopping_scam"
    OTHER = "other"


# ════════════════════════════════════════════════════════════════════════════
# ANALYZER — /api/v1/analyze
# ════════════════════════════════════════════════════════════════════════════

class AnalyzeRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        description="Teks pesan mencurigakan yang ingin dianalisis",
        examples=["Selamat! Nomor Anda terpilih sebagai pemenang hadiah Rp 50 juta."],
    )


class AnalyzeResponse(BaseModel):
    scam_probability:        float      = Field(..., ge=0.0, le=1.0)
    manipulation_techniques: list[str]  = Field(default_factory=list)
    risk_level:              RiskLevel
    educational_tip:         str
    analyzed_message:        str        = Field(..., description="Pesan asli yang dianalisis")


# ════════════════════════════════════════════════════════════════════════════
# SIMULATOR — /api/v1/simulate
# ════════════════════════════════════════════════════════════════════════════

class ChatMessage(BaseModel):
    role:    str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=2000)


class SimulateRequest(BaseModel):
    scenario: str | None = None
    user_message: str | None = None
    session_id: str | None = None

class SimulateResponse(BaseModel):
    session_id: str
    scammer_message: str
    red_flags: list[str] = []
    tip: str = ""
    is_reveal: bool = False


# ════════════════════════════════════════════════════════════════════════════
# REPORT — /api/v1/report
# ════════════════════════════════════════════════════════════════════════════

class ReportCreate(BaseModel):
    phone_number: str | None = None
    bank_account: str | None = None
    scam_category: ScamCategory
    description: str
    evidence_url: str | None = None
    reporter_alias: str | None = None

class ReportResponse(BaseModel):
    id: int
    phone_number: str | None = None
    bank_account: str | None = None
    scam_category: str
    description: str
    evidence_url: str | None = None
    reporter_alias: str | None = None
    risk_score: float = 25.0
    report_count: int = 1
    created_at: Any = None

    class Config:
        from_attributes = True


# ════════════════════════════════════════════════════════════════════════════
# GENERIC
# ════════════════════════════════════════════════════════════════════════════

class HealthResponse(BaseModel):
    status:  str = "ok"
    version: str
    env:     str


class ErrorResponse(BaseModel):
    detail:    str
    error_code: str | None = None
