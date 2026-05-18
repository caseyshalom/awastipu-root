from fastapi import APIRouter
from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
    """Endpoint untuk memverifikasi bahwa API berjalan normal."""
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        env=settings.ENVIRONMENT,
    )
