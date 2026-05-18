"""
Vision Service — OCR & analisis gambar screenshot chat.
Menggunakan Tesseract OCR atau Gemini Vision untuk extract teks dari gambar.
"""

import io
from typing import Optional

from app.core.config import settings


async def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract teks dari gambar menggunakan OCR.
    Prioritas: Gemini Vision API → Tesseract OCR fallback.
    """
    if settings.GEMINI_API_KEY:
        return await _extract_with_gemini_vision(image_bytes)
    return _extract_with_tesseract(image_bytes)


async def _extract_with_gemini_vision(image_bytes: bytes) -> str:
    """Gunakan Gemini Vision untuk extract dan analisis teks dari gambar."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)

        prompt = (
            "Ekstrak semua teks yang terlihat dalam gambar ini. "
            "Jika ini screenshot percakapan chat, susun teks secara kronologis. "
            "Berikan output berupa teks saja tanpa penjelasan tambahan."
        )

        response = await model.generate_content_async([
            prompt,
            {"mime_type": "image/png", "data": image_bytes},
        ])

        return response.text.strip()
    except Exception as e:
        print(f"[Vision] Gemini Vision error, falling back to Tesseract: {e}")
        return _extract_with_tesseract(image_bytes)


def _extract_with_tesseract(image_bytes: bytes) -> str:
    """Fallback OCR menggunakan Tesseract."""
    try:
        from PIL import Image
        import pytesseract

        image = Image.open(io.BytesIO(image_bytes))
        # Konfigurasi untuk Bahasa Indonesia + English
        text = pytesseract.image_to_string(image, lang="ind+eng")
        return text.strip()
    except Exception as e:
        print(f"[Vision] Tesseract error: {e}")
        return ""


async def analyze_screenshot(image_bytes: bytes) -> dict:
    """
    Pipeline lengkap: Extract teks → kembalikan untuk dianalisis.
    """
    extracted_text = await extract_text_from_image(image_bytes)

    if not extracted_text:
        return {
            "success": False,
            "text": "",
            "message": "Tidak dapat mengekstrak teks dari gambar. Coba foto yang lebih jelas.",
        }

    return {
        "success": True,
        "text": extracted_text,
        "message": f"Berhasil mengekstrak {len(extracted_text)} karakter dari gambar.",
    }
