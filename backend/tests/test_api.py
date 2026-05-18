"""
Unit tests untuk AwasTipu API.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture
def client():
    """Async HTTP client untuk testing."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# ═══════════════════════════════════════════════
# Health Check
# ═══════════════════════════════════════════════

@pytest.mark.asyncio
async def test_health_check(client):
    async with client as c:
        response = await c.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "awastipu-api"


# ═══════════════════════════════════════════════
# Analyze Endpoints
# ═══════════════════════════════════════════════

@pytest.mark.asyncio
async def test_analyze_safe_text(client):
    async with client as c:
        response = await c.post("/api/v1/analyze/text", json={
            "text": "Halo, apa kabar? Besok jadi ketemuan di kafe?",
            "include_tactics": True,
        })
    assert response.status_code == 200
    data = response.json()
    assert "risk_level" in data
    assert data["risk_score"] <= 30  # Pesan aman seharusnya skor rendah


@pytest.mark.asyncio
async def test_analyze_scam_text(client):
    async with client as c:
        response = await c.post("/api/v1/analyze/text", json={
            "text": "SELAMAT! Anda menang undian Rp 100juta! Kirim OTP dan transfer biaya admin sekarang juga ke rekening BCA!",
            "include_tactics": True,
        })
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 50  # Pesan scam harus skor tinggi
    assert len(data["tactics"]) > 0


@pytest.mark.asyncio
async def test_analyze_short_text_rejected(client):
    async with client as c:
        response = await c.post("/api/v1/analyze/text", json={
            "text": "hi",
            "include_tactics": False,
        })
    assert response.status_code == 422  # Validation error (min_length=5)


# ═══════════════════════════════════════════════
# Simulator Endpoints
# ═══════════════════════════════════════════════

@pytest.mark.asyncio
async def test_start_simulation(client):
    async with client as c:
        response = await c.post("/api/v1/simulate/start", json={
            "scenario": "phishing",
        })
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["scammer_message"]) > 0
    assert len(data["red_flags"]) > 0


@pytest.mark.asyncio
async def test_list_scenarios(client):
    async with client as c:
        response = await c.get("/api/v1/simulate/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert len(data["scenarios"]) >= 5


# ═══════════════════════════════════════════════
# Reports Endpoints
# ═══════════════════════════════════════════════

@pytest.mark.asyncio
async def test_search_without_params(client):
    async with client as c:
        response = await c.get("/api/v1/reports/search")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
