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
Kamu adalah sistem analisis keamanan pesan digital untuk aplikasi AwasTipu.
Tugasmu adalah menganalisis pesan yang diterima pengguna dan menentukan apakah
pesan tersebut merupakan upaya penipuan (scam/fraud).

OUTPUT WAJIB dalam format JSON valid dengan struktur berikut:
{
  "scam_probability": <float antara 0.0 hingga 1.0>,
  "manipulation_techniques": [<list string teknik manipulasi yang terdeteksi>],
  "risk_level": "<AMAN | WASPADA | BAHAYA>",
  "educational_tip": "<string saran singkat untuk orang awam>"
}

PANDUAN PENILAIAN:
- scam_probability 0.0–0.3  → risk_level: "AMAN"
- scam_probability 0.3–0.7  → risk_level: "WASPADA"
- scam_probability 0.7–1.0  → risk_level: "BAHAYA"

TEKNIK MANIPULASI YANG DIKENALI:
- "Urgency"           : menciptakan tekanan waktu ("segera", "1x24 jam", "hari ini")
- "Fear-mongering"    : menakut-nakuti ("akun diblokir", "terkena virus", "masalah hukum")
- "Fake Rewards"      : iming-iming hadiah palsu ("selamat menang", "terpilih")
- "Authority Spoofing": menyamar sebagai institusi resmi (bank, pemerintah, kurir)
- "APK Phishing"      : meminta install APK tidak resmi
- "OTP Harvesting"    : meminta kode OTP, PIN, atau password
- "Social Proof"      : mengklaim banyak orang sudah ikut/percaya
- "Reciprocity"       : memberi sesuatu kecil untuk minta sesuatu besar
- "Impersonation"     : menyamar sebagai orang yang dikenal korban

Berikan educational_tip dalam Bahasa Indonesia yang mudah dipahami orang awam.
Jangan tambahkan teks apapun di luar JSON.
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
    Analisis pesan mencurigakan dan kembalikan risk assessment.

    Args:
        user_message: Teks pesan yang ingin dianalisis.

    Returns:
        Dict dengan struktur:
        {
            "scam_probability"      : float (0.0 – 1.0),
            "manipulation_techniques": list[str],
            "risk_level"            : "AMAN" | "WASPADA" | "BAHAYA",
            "educational_tip"       : str
        }

    Raises:
        RuntimeError : Jika panggilan ke LLM gagal.
        ValueError   : Jika respons LLM tidak dapat di-parse sebagai JSON.
    """
    prompt = (
        f"{_ANALYZER_SYSTEM_PROMPT}\n\n"
        f"PESAN YANG DIANALISIS:\n\"\"\"\n{user_message}\n\"\"\""
    )

    try:
        response = _model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.1,        # rendah agar output konsisten & deterministik
                max_output_tokens=512,
            ),
        )
        raw_text = response.text.strip()
        logger.debug("analyze_message_intent raw response: %s", raw_text[:200])

        result = _extract_json(raw_text)

        # ── Validasi & normalisasi output ────────────────────────────────
        scam_prob = float(result.get("scam_probability", 0.0))
        scam_prob = max(0.0, min(1.0, scam_prob))  # clamp ke [0, 1]

        techniques = result.get("manipulation_techniques", [])
        if not isinstance(techniques, list):
            techniques = [str(techniques)]

        risk_level = result.get("risk_level", "WASPADA").upper()
        if risk_level not in {"AMAN", "WASPADA", "BAHAYA"}:
            # Fallback berdasarkan probability jika LLM memberi nilai tidak valid
            if scam_prob < 0.3:
                risk_level = "AMAN"
            elif scam_prob < 0.7:
                risk_level = "WASPADA"
            else:
                risk_level = "BAHAYA"

        educational_tip = result.get(
            "educational_tip",
            "Selalu verifikasi identitas pengirim sebelum mengambil tindakan apapun."
        )

        normalized: dict[str, Any] = {
            "scam_probability":       round(scam_prob, 3),
            "manipulation_techniques": techniques,
            "risk_level":             risk_level,
            "educational_tip":        str(educational_tip),
        }

        logger.info(
            "analyze_message_intent: risk=%s prob=%.3f techniques=%s",
            risk_level, scam_prob, techniques
        )
        return normalized

    except ValueError:
        raise
    except Exception as exc:
        logger.error("analyze_message_intent gagal: %s", exc, exc_info=True)
        raise RuntimeError(f"AI Agent error: {exc}") from exc


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
    except Exception:
        analysis = {
            "manipulation_techniques": ["Urgensi Palsu"],
            "educational_tip": "Jangan terburu-buru merespons pesan yang meminta data pribadi."
        }
    
    return {
        "session_id": session_id,
        "scammer_message": scammer_msg,
        "red_flags": analysis.get("manipulation_techniques", []),
        "tip": analysis.get("educational_tip", ""),
        "is_reveal": len(history) >= 8  # Selesai setelah 4 putaran chat
    }
