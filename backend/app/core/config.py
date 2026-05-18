"""
Konfigurasi aplikasi menggunakan Pydantic BaseSettings.
Semua nilai dibaca dari environment variables / file .env.
"""

from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────
    APP_NAME: str = "AwasTipu"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development | staging | production

    # ── API ──────────────────────────────────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── AI Provider ──────────────────────────────────────────────────────
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""          # opsional, fallback
    GEMINI_MODEL: str = "gemini-2.0-flash"
    AI_MODEL: str = "gemini-2.0-flash"
    AI_MAX_TOKENS: int = 1024
    AI_TEMPERATURE: float = 0.7

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: Any) -> str:
        if not v:
            import os
            v = os.getenv("SUPABASE_DATABASE_URL") or os.getenv("DATABASE_URL")
        
        if not v or not isinstance(v, str):
            return "sqlite+aiosqlite:///./awastipu.db"
            
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
            
        return v

    # ── Security ─────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-this-in-production-use-openssl-rand-hex-32"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 jam

    # ── Rate Limiting ────────────────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 30


# Singleton — import ini di seluruh aplikasi
settings = Settings()
