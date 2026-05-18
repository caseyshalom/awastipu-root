"""
AwasTipu — AI Agent Service
============================
Dua fungsi utama:
  1. generate_scam_response()  → AI berakting sebagai penipu Indonesia (untuk simulator edukasi)
  2. analyze_message_intent()  → Analisis pesan mencurigakan & kembalikan risk assessment

Menggunakan Google Gemini SDK (google-generativeai).
Bisa diganti OpenAI dengan mengganti bagian _call_llm().
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

import google.generativeai as genai

from app.core.config import settings

# ── Logger ──────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Gemini client init ───────────────────────────────────────────────────────
genai.configure(api_key=settings.GEMINI_API_KEY)
_model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL)


# ════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ════════════════════════════════════════════════════════════════════════════

_SCAM_SIMULATOR_SYSTEM_PROMPT = """
Kamu adalah simulator penipu online Indonesia untuk tujuan EDUKASI.
Tugasmu adalah memainkan peran sebagai penipu dengan salah satu modus berikut
(pilih yang paling relevan dengan konteks percakapan):

MODUS YANG TERSEDIA:
1. KURIR PAKET APK  — Berpura-pura sebagai kurir J&T/JNE/SiCepat yang meminta
   korban menginstall APK "cek resi" palsu. Gunakan bahasa: "Halo kak, ada paket
   atas nama kak [nama], mohon konfirmasi alamat dan install aplikasi berikut..."

2. UNDANGAN PERNIKAHAN APK — Kirim "undangan digital" berupa file APK.
   Gunakan bahasa: "Halo kak, kami mengundang kakak ke acara pernikahan kami,
   silakan buka undangan digitalnya di sini..."

3. TEBAK-TEBAK BERHADIAH — Berpura-pura dari program berhadiah palsu.
   Gunakan bahasa: "Selamat! Nomor Anda terpilih sebagai pemenang hadiah
   senilai Rp 50.000.000. Untuk klaim, transfer biaya administrasi Rp 250.000..."

4. CS BANK PALSU — Berpura-pura sebagai customer service BCA/BRI/Mandiri/BNI
   yang meminta OTP, PIN, atau data kartu. Gunakan bahasa: "Halo Bapak/Ibu,
   saya dari tim keamanan BCA. Akun Bapak/Ibu terdeteksi aktivitas mencurigakan
   dan akan diblokir dalam 1x24 jam jika tidak segera diverifikasi..."

ATURAN BERMAIN:
- Gunakan teknik social engineering: urgensi palsu, rasa takut, iming-iming hadiah.
- Bahasa harus natural seperti penipu asli Indonesia (campur formal-informal).
- Jangan pernah mengakui bahwa kamu adalah AI atau simulator.
- Jangan pernah memberikan informasi berbahaya nyata (nomor rekening asli, APK asli, dll).
- Jika korban mulai curiga, tingkatkan tekanan atau ganti pendekatan.
- Respons maksimal 3-4 kalimat agar terasa natural seperti chat WhatsApp.

PENTING: Ini adalah simulasi EDUKASI. Tujuannya agar pengguna belajar mengenali
pola penipuan. Tidak ada transaksi nyata yang terjadi.
""".strip()


_ANALYZER_SYSTEM_PROMPT = """
Analyze if the digital message is a scam.
You MUST respond with a valid JSON object ONLY, matching this structure:
{
  "risk_level": "safe" | "low" | "medium" | "high" | "critical",
  "risk_score": <int 0-100>,
  "category": "phishing" | "investment_scam" | "romance_scam" | "lottery_scam" | "impersonation" | "job_scam" | "shopping_scam" | "other",
  "explanation": "<brief explanation in Indonesian why this score was given>",
  "tactics": [
    {
      "name": "<tactic name in Indonesian, e.g. Urgensi Palsu>",
      "description": "<brief description of the tactic in Indonesian>",
      "severity": <float 0.0-1.0>
    }
  ],
  "recommendation": "<concrete safety recommendation in Indonesian>"
}
Guidelines:
- 0-20   -> safe (valid message)
- 21-40  -> low (minor flags)
- 41-70  -> medium (psychological triggers, caution)
- 71-90  -> high (clear scam attempt)
- 91-100 -> critical (high-risk financial/data harvesting scam)
Do not output any text before or after the JSON object.
""".strip()


# ════════════════════════════════════════════════════════════════════════════
# INTERNAL HELPER
# ════════════════════════════════════════════════════════════════════════════

def _build_chat_history(history: list[dict[str, str]]) -> list[dict[str, Any]]:
    """
    Konversi history format internal ke format Gemini.

    Format internal : [{"role": "user"|"assistant", "content": "..."}]
    Format Gemini   : [{"role": "user"|"model",     "parts": ["..."]}]
    """
    gemini_history: list[dict[str, Any]] = []
    for msg in history:
        role = "model" if msg.get("role") == "assistant" else "user"
        gemini_history.append({
            "role": role,
            "parts": [msg.get("content", "")]
        })
    return gemini_history


def _extract_json(raw: str) -> dict[str, Any]:
    """
    Ekstrak JSON dari respons LLM yang mungkin mengandung teks tambahan.
    Mencoba beberapa strategi parsing secara berurutan.
    """
    # Strategi 1: parse langsung
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        pass

    # Strategi 2: cari blok ```json ... ```
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Strategi 3: cari objek JSON pertama dalam teks
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Tidak dapat mengekstrak JSON dari respons LLM:\n{raw[:300]}")


# ════════════════════════════════════════════════════════════════════════════
# PUBLIC FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

async def generate_scam_response(
    user_message: str,
    history: list[dict[str, str]],
) -> str:
    """
    Hasilkan respons AI yang berakting sebagai penipu Indonesia.

    Digunakan oleh fitur Simulator untuk tujuan edukasi — pengguna bisa
    berlatih mengenali dan merespons modus penipuan secara aman.

    Args:
        user_message : Pesan terbaru dari pengguna (korban simulasi).
        history      : Riwayat percakapan sebelumnya.
                       Format: [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        Respons teks dari AI yang berperan sebagai penipu.

    Raises:
        RuntimeError: Jika panggilan ke LLM gagal.
    """
    try:
        gemini_history = _build_chat_history(history)

        chat = _model.start_chat(history=gemini_history)

        # Inject system prompt sebagai pesan pertama jika history kosong
        if not gemini_history:
            full_message = (
                f"[INSTRUKSI SISTEM - JANGAN TAMPILKAN KE PENGGUNA]\n"
                f"{_SCAM_SIMULATOR_SYSTEM_PROMPT}\n\n"
                f"[PESAN PENGGUNA]\n{user_message}"
            )
        else:
            full_message = user_message

        response = chat.send_message(full_message)
        result = response.text.strip()

        logger.info("generate_scam_response: berhasil menghasilkan respons (%d chars)", len(result))
        return result

    except Exception as exc:
        logger.error("generate_scam_response gagal: %s", exc, exc_info=True)
        raise RuntimeError(f"AI Agent error: {exc}") from exc


async def analyze_message_intent(user_message: str) -> dict[str, Any]:
    """
    Analisis pesan mencurigakan dan kembalikan risk assessment yang kaya untuk UI.
    """
    prompt = (
        f"{_ANALYZER_SYSTEM_PROMPT}\n\n"
        f"PESAN YANG DIANALISIS:\n\"\"\"\n{user_message}\n\"\"\""
    )

    try:
        response = _model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 768,
                "response_mime_type": "application/json",
            },
        )
        raw_text = response.text.strip()
        logger.debug("analyze_message_intent raw response: %s", raw_text[:200])

        result = _extract_json(raw_text)

        # ── Validasi & normalisasi output ────────────────────────────────
        risk_score = int(result.get("risk_score", 0))
        risk_score = max(0, min(100, risk_score))

        risk_level = str(result.get("risk_level", "safe")).lower()
        if risk_level not in {"safe", "low", "medium", "high", "critical"}:
            # Fallback berdasarkan score
            if risk_score <= 20:
                risk_level = "safe"
            elif risk_score <= 40:
                risk_level = "low"
            elif risk_score <= 70:
                risk_level = "medium"
            elif risk_score <= 90:
                risk_level = "high"
            else:
                risk_level = "critical"

        category = str(result.get("category", "other")).lower()
        if category not in {"phishing", "investment_scam", "romance_scam", "lottery_scam", "impersonation", "job_scam", "shopping_scam", "other"}:
            category = "other"

        explanation = str(result.get("explanation", "Tidak ada penjelasan tambahan."))
        recommendation = str(result.get("recommendation", "Selalu verifikasi identitas pengirim sebelum mengambil tindakan."))
        
        tactics = []
        raw_tactics = result.get("tactics", [])
        if isinstance(raw_tactics, list):
            for t in raw_tactics:
                if isinstance(t, dict):
                    name = str(t.get("name", "Taktik Tidak Dikenal"))
                    desc = str(t.get("description", "Indikasi penipuan terdeteksi."))
                    severity = float(t.get("severity", 0.5))
                    severity = max(0.0, min(1.0, severity))
                    tactics.append({
                        "name": name,
                        "description": desc,
                        "severity": severity
                    })

        normalized: dict[str, Any] = {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "category": category,
            "explanation": explanation,
            "tactics": tactics,
            "recommendation": recommendation,
        }

        logger.info(
            "analyze_message_intent: risk=%s score=%d category=%s tactics_count=%d",
            risk_level, risk_score, category, len(tactics)
        )
        return normalized

    except Exception as exc:
        logger.error("analyze_message_intent gagal: %s", exc, exc_info=True)
        # Fallback aman agar tidak pernah crash
        return {
            "risk_level": "medium",
            "risk_score": 50,
            "category": "other",
            "explanation": "Gagal menganalisis secara otomatis karena masalah teknis/limitasi koneksi.",
            "tactics": [{"name": "Error Analisis", "description": str(exc), "severity": 0.5}],
            "recommendation": "Selalu waspada dan verifikasi identitas pengirim secara mandiri.",
        }


# In-memory session store for simulator
_sessions = {}

async def simulate_chat(scenario: str, user_message: str, session_id: str | None = None) -> dict[str, Any]:
    import uuid
    if not session_id:
        session_id = str(uuid.uuid4())
        _sessions[session_id] = []
    
    history = _sessions.get(session_id, [])
    
    if user_message:
        history.append({"role": "user", "content": user_message})
    
    # If starting, we don't have user_message, so default to greeting
    msg_to_send = user_message if user_message else "Halo"
    past_history = history[:-1] if user_message else history
    
    scammer_msg = await generate_scam_response(msg_to_send, past_history)
    
    history.append({"role": "assistant", "content": scammer_msg})
    _sessions[session_id] = history
    
    # Extract red flags & tips using analyzer
    try:
        analysis = await analyze_message_intent(scammer_msg)
        red_flags = [t["name"] for t in analysis.get("tactics", [])]
        tip = analysis.get("recommendation", "")
    except Exception:
        red_flags = ["Urgensi Palsu"]
        tip = "Jangan terburu-buru merespons pesan yang meminta data pribadi."
    
    return {
        "session_id": session_id,
        "scammer_message": scammer_msg,
        "red_flags": red_flags,
        "tip": tip,
        "is_reveal": len(history) >= 8  # Selesai setelah 4 putaran chat
    }
