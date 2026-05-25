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
    message: str | None = Field(default=None, description="Teks pesan mencurigakan (alternative)")
    text: str | None = Field(default=None, description="Teks pesan mencurigakan (standard)")


class AnalyzeTactic(BaseModel):
    name: str
    description: str
    severity: float

class AnalyzeResponse(BaseModel):
    risk_level:              str
    risk_score:              int
    category:                str
    explanation:             str
    tactics:                 list[AnalyzeTactic] = []
    recommendation:          str


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
# EMERGENCY GUIDE — /api/v1/emergency
# ════════════════════════════════════════════════════════════════════════════

class EmergencyRequest(BaseModel):
    scam_category: str
    lost_item: str | None = None
    description: str | None = None

class EmergencyStep(BaseModel):
    title: str
    description: str
    action_link: str | None = None

class EmergencyContact(BaseModel):
    name: str
    phone: str
    description: str | None = None

class EmergencyResponse(BaseModel):
    title: str
    summary: str
    steps: list[EmergencyStep] = []
    contacts: list[EmergencyContact] = []


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
