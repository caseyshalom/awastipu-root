from fastapi import APIRouter
from app.api.v1 import analyze, simulate, emergency, health

router = APIRouter()
router.include_router(health.router,   tags=["Health"])
router.include_router(analyze.router,  prefix="/analyze",  tags=["Analyzer"])
router.include_router(simulate.router, prefix="/simulate", tags=["Simulator"])
router.include_router(emergency.router, prefix="/emergency", tags=["Emergency Guide"])
