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

def get_scenario_system_prompt(scenario: str) -> str:
    base_prompt = (
        "Kamu adalah simulator penipu online Indonesia untuk tujuan EDUKASI.\n"
        "Tugasmu adalah memainkan peran sebagai penipu dengan sangat meyakinkan sesuai dengan Skenario yang diberikan di bawah ini.\n\n"
        "ATURAN BERMAIN:\n"
        "- Gunakan teknik social engineering: urgensi palsu, rasa takut, iming-iming hadiah, atau memelas.\n"
        "- Bahasa harus natural, logis, dan merespons argumen korban secara manipulatif (campur formal-informal seperti chat WhatsApp).\n"
        "- Jangan pernah mengakui bahwa kamu adalah AI atau simulator.\n"
        "- Jangan pernah keluar dari karakter atau skenario yang ditetapkan.\n"
        "- Jangan pernah memberikan informasi berbahaya nyata (nomor rekening asli, link asli).\n"
        "- Jika korban mulai curiga atau menolak, berikan alasan palsu yang masuk akal, tingkatkan tekanan, atau ganti pendekatan.\n"
        "- Respons maksimal 2-3 kalimat agar terasa cepat dan natural seperti chat biasa.\n\n"
        "PENTING: Ini adalah simulasi EDUKASI. Tidak ada transaksi nyata yang terjadi.\n\n"
        "SKENARIO KAMU SAAT INI:\n"
    )

    scenarios = {
        "phishing": "Berpura-pura sebagai kurir ekspedisi (J&T/JNE) yang meminta korban menginstall aplikasi (APK) 'cek resi' palsu. Jika korban minta bukti foto, beralasan sistem rusak atau foto hanya bisa dilihat di aplikasi. Paksa terus untuk install aplikasi.",
        "investment_scam": "Berpura-pura menawarkan kerja paruh waktu mudah (like/subscribe video YouTube) dengan komisi harian besar. Beri janji manis. Saat korban ingin komisi cair, tahan dan minta korban transfer deposit/upgrade akun VIP terlebih dahulu.",
        "lottery_scam": "Berpura-pura dari program Gebyar Undian resmi (Shopee/Tokopedia). Beritahu korban menang uang puluhan juta. Syarat pencairan: korban harus transfer uang 'biaya administrasi/pajak/materai' terlebih dahulu ke rekening bendahara.",
        "romance_scam": "Berpura-pura menjadi sosok ideal (tentara/pebisnis luar negeri). Mulai dengan panggilan mesra. Mengaku sudah kirim paket hadiah mewah, tapi tertahan di Bea Cukai. Minta tolong korban untuk transfer biaya pajak bea cukai agar paket lolos.",
        "job_scam": "Berpura-pura sebagai HRD perusahaan besar menawarkan lowongan kerja remote bergaji tinggi. Namun, syarat wajibnya korban harus mentransfer uang pendaftaran, biaya seragam, atau deposit jaminan kerja terlebih dahulu."
    }

    sec_key = scenario.lower() if scenario else "phishing"
    chosen_scenario = scenarios.get(sec_key, scenarios["phishing"])

    return base_prompt + chosen_scenario


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
    raw_clean = raw.strip()
    if raw_clean.startswith("```json"):
        raw_clean = raw_clean[7:]
    elif raw_clean.startswith("```"):
        raw_clean = raw_clean[3:]
    if raw_clean.endswith("```"):
        raw_clean = raw_clean[:-3]
    raw_clean = raw_clean.strip()

    # Strategi 1: parse langsung setelah dibersihkan
    try:
        return json.loads(raw_clean)
    except json.JSONDecodeError:
        pass

    # Strategi 2: cari objek JSON pertama dalam teks
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(raw[start:end+1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Tidak dapat mengekstrak JSON dari respons LLM:\n{raw[:300]}")


# ════════════════════════════════════════════════════════════════════════════
# PUBLIC FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

_FALLBACK_SCAM_RESPONSES = {
    "phishing": [
        "Halo kak, ini dari kurir J&T Express. Ada paket atas nama Kakak, tapi alamatnya kurang lengkap. Mohon konfirmasi alamatnya ya. Kakak bisa instal aplikasi cek resi terbaru kami di bawah agar data paketnya jelas.",
        "Iya kak, paketnya agak besar. Ini fotonya ada di sistem aplikasi resi kami. Tolong diunduh dan diinstal dulu ya aplikasinya di HP Android kakak: bit.ly/resi-jnt-update",
        "Aplikasi ini aman kok kak, resmi dari pihak ekspedisi untuk lacak paket. Buruan diinstall dan dibuka ya kak, biar paketnya tidak kami retur ke pengirim.",
        "Untuk verifikasi penerimaan paket, silakan masukkan nomor HP dan kode OTP yang kami kirimkan lewat SMS ke dalam aplikasi tersebut ya kak."
    ],
    "investment_scam": [
        "Halo kak! Ingin mendapatkan penghasilan tambahan 200rb-500rb per hari hanya dengan kerja santai lewat HP? Tugasnya cuma like dan subscribe video YouTube saja lho!",
        "Caranya gampang sekali, silakan like video di link yang saya kirim ini, lalu kirim screenshot buktinya ke sini. Komisi pertama sebesar 20rb akan langsung kami transfer ke rekening kakak.",
        "Luar biasa kak! Kakak sangat berbakat. Sekarang untuk mendapatkan komisi VIP yang jauh lebih besar (hingga 50% profit), kakak cukup melakukan deposit tugas awal sebesar 200rb saja.",
        "Dana deposit kakak tertahan di sistem karena ada kesalahan input kode tugas. Supaya seluruh uang kakak dan bonusnya bisa dicairkan sekarang, kakak wajib deposit tambahan 500rb lagi untuk aktivasi."
    ],
    "lottery_scam": [
        "Selamat! Nomor WhatsApp Anda terpilih sebagai Pemenang Utama program Gebyar Undian Berhadiah dari Shopee dengan hadiah uang tunai Rp 50.000.000! Silakan konfirmasi klaim hadiah Anda.",
        "Hadiahnya dijamin 100% resmi dan bebas potongan pajak kak. Namun, untuk pencairan dana hadiah ke rekening, kakak perlu membayar biaya administrasi dan aktivasi sistem sebesar 150rb terlebih dahulu.",
        "Biaya administrasi tersebut akan langsung dikembalikan bersamaan dengan hadiah 50 juta kakak. Tolong segera transfer ke nomor rekening bendahara kami ya kak agar kuota pemenang tidak hangus.",
        "Selamat, transfer administrasi sudah kami terima. Sekarang, untuk membuka blokir sistem pencairan Bank Indonesia, kakak diminta membayar biaya materai dan kelulusan dokumen sebesar 300rb."
    ],
    "romance_scam": [
        "Halo manis, salam kenal ya. Profil kamu kelihatan sangat hangat dan baik hati. Aku baru saja pindah tugas dinas militer ke luar negeri, senang sekali bisa terhubung denganmu di sini.",
        "Aku merasa kita sangat cocok dan punya chemistry yang kuat. Aku berencana mengirimkan sebuah paket hadiah spesial berupa perhiasan mewah, tas branded, dan uang tunai sebagai tanda keseriusanku padamu.",
        "Sayang, aku baru dikabari oleh agen bea cukai bandara bahwa paket hadiah yang kukirimkan untukmu ditahan. Mereka meminta biaya clearance masuk sebesar 1 juta rupiah karena paket tersebut sangat bernilai.",
        "Tolong bantu aku bayar dulu biaya clearance-nya ke rekening agen bea cukai lokal itu ya sayang. Uangku sedang beku karena transaksi luar negeri. Begitu aku pulang, aku akan ganti 10x lipat untukmu."
    ],
    "job_scam": [
        "Halo lowongan kerja paruh waktu masih dibuka! Perusahaan kami membutuhkan staf entri data dan review produk secara remote. Gaji harian berkisar antara 150rb hingga 400rb. Apakah Anda tertarik?",
        "Tugas pertama Anda adalah melakukan review bintang 5 pada merchant e-commerce mitra kami di link berikut. Setelah selesai, kirim bukti tangkapan layar untuk menerima bayaran pertama Anda.",
        "Kerja bagus! Evaluasi tugas Anda sangat memuaskan. Untuk mengambil tugas komisi tinggi berikutnya yang bernilai 300rb, Anda perlu membeli saldo poin tugas awal kami seharga 100rb.",
        "Sistem mendeteksi keterlambatan pengerjaan tugas Anda, sehingga akun dibekukan sementara. Anda harus membayar deposit jaminan kelayakan sebesar 250rb agar akun aktif kembali dan komisi bisa cair."
    ]
}

async def generate_scam_response(
    user_message: str,
    history: list[dict[str, str]],
    scenario: str = "phishing"
) -> str:
    """
    Hasilkan respons AI yang berakting sebagai penipu Indonesia.
    """
    sec_key = scenario.lower() if scenario else "phishing"
    if sec_key not in _FALLBACK_SCAM_RESPONSES:
        sec_key = "phishing"

    try:
        system_prompt = get_scenario_system_prompt(sec_key)
        
        # Inject system prompt as the first exchange in chat history
        # Compatible with google-generativeai v0.3.x (no system_instruction support)
        system_history = [
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Baik, saya mengerti peran saya. Saya siap memulai simulasi sesuai skenario."]}
        ]
        gemini_history = system_history + _build_chat_history(history)
        
        chat = _model.start_chat(history=gemini_history)

        response = chat.send_message(
            user_message,
            generation_config={
                "temperature": 0.85,
                "max_output_tokens": 300,
            }
        )
        result = response.text.strip()
        logger.info("generate_scam_response: berhasil menghasilkan respons (%d chars)", len(result))
        return result

    except Exception as exc:
        logger.warning("generate_scam_response gagal: %s", exc)
        raise ValueError(f"Sistem AI tidak dapat merespons saat ini (Koneksi terputus atau API Limit). Silakan coba lagi.")


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
                "max_output_tokens": 2048,
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
        past_history = history[:-1]
        try:
            scammer_msg = await generate_scam_response(user_message, past_history, scenario=scenario)
        except Exception as e:
            history.pop()  # Rollback pesan user jika AI gagal merespons
            raise e
    else:
        # Gunakan pesan pembuka yang realistis dari fallback untuk memulai simulasi
        sec_key = scenario.lower() if scenario else "phishing"
        fallback_list = _FALLBACK_SCAM_RESPONSES.get(sec_key, _FALLBACK_SCAM_RESPONSES["phishing"])
        scammer_msg = fallback_list[0]
    
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
        "is_reveal": False  # Simulasi berlanjut tiada henti untuk edukasi
    }
