"""
Route: Analisis teks/gambar scam
POST /api/v1/analyze/text   — Analisis teks pesan
POST /api/v1/analyze/image  — Upload & analisis screenshot
"""

from fastapi import APIRouter, Request, UploadFile, File

from app.core.security import rate_limiter, sanitize_text
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.ai_agent import analyze_message_intent
from app.services.vision import analyze_screenshot

router = APIRouter()


@router.post("/text", response_model=AnalyzeResponse)
async def analyze_text_endpoint(request: Request, body: AnalyzeRequest):
    """
    Analisis teks pesan untuk mendeteksi potensi penipuan.
    Mengembalikan skor risiko, kategori, dan penjelasan detail.
    """
    rate_limiter.check(request)
    cleaned_text = sanitize_text(body.message)
    result = await analyze_message_intent(cleaned_text)
    # response expects AnalyzeResponse, which has scam_probability, manipulation_techniques, risk_level, educational_tip, analyzed_message.
    # result has scam_probability, manipulation_techniques, risk_level, educational_tip.
    # We need to add analyzed_message to it.
    result["analyzed_message"] = cleaned_text
    return result


@router.post("/image")
async def analyze_image_endpoint(request: Request, file: UploadFile = File(...)):
    """
    Upload screenshot chat → OCR extract teks → analisis otomatis.
    Mendukung format: PNG, JPG, JPEG, WEBP.
    """
    rate_limiter.check(request)

    # Validasi tipe file
    allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        return {"error": "Format file tidak didukung. Gunakan PNG, JPG, atau WEBP."}

    # Baca image bytes
    image_bytes = await file.read()

    # Limit ukuran file (5MB)
    if len(image_bytes) > 5 * 1024 * 1024:
        return {"error": "Ukuran file terlalu besar. Maksimal 5MB."}

    # Extract teks & analisis
    ocr_result = await analyze_screenshot(image_bytes)

    if not ocr_result["success"]:
        return ocr_result

    # Analisis teks yang sudah di-extract
    analysis = await analyze_message_intent(ocr_result["text"])
    return {
        "extracted_text": ocr_result["text"],
        "analysis": analysis,
    }
