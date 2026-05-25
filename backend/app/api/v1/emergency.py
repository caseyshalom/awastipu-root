from fastapi import APIRouter, Request
from app.core.security import rate_limiter
from app.models.schemas import EmergencyRequest, EmergencyResponse, EmergencyStep, EmergencyContact

router = APIRouter()

@router.post("/guide", response_model=EmergencyResponse)
async def generate_emergency_guide(
    request: Request,
    body: EmergencyRequest,
):
    """
    Generate langkah-langkah darurat (Emergency Guide) 
    berdasarkan jenis penipuan dan item yang terdampak.
    """
    rate_limiter.check(request)
    
    category = body.scam_category.lower()
    lost = (body.lost_item or "").lower()
    
    # Default kontak
    contacts = [
        EmergencyContact(
            name="Call Center Polisi (Cyber Crime)", 
            phone="110", 
            description="Layanan pengaduan darurat kejahatan siber"
        ),
        EmergencyContact(
            name="Aduan Nomor (Kominfo)", 
            phone="159", 
            description="Aduan nomor telepon yang terindikasi penipuan"
        )
    ]
    
    steps = []
    
    if "phishing" in category or "uang" in lost or "money" in lost or "account" in lost:
        title = "Panduan Darurat: Kebocoran Data / Finansial"
        summary = "Segera amankan aset finansial dan data pribadi Anda. Waktu sangat krusial."
        
        steps.append(EmergencyStep(
            title="Blokir Kartu dan Rekening",
            description="Segera hubungi bank Anda untuk memblokir kartu ATM/Kredit dan membekukan sementara rekening Anda. (Pastikan menelepon Call Center resmi bank Anda, biasanya nomor tertera di belakang kartu ATM).",
        ))
        steps.append(EmergencyStep(
            title="Ubah Password dan Aktifkan 2FA",
            description="Ubah password email utama dan akun perbankan Anda. Aktifkan otentikasi dua langkah (2FA)."
        ))
        steps.append(EmergencyStep(
            title="Simpan Bukti Transaksi/Chat",
            description="Screenshot semua percakapan, bukti transfer, dan URL website penipu sebelum dihapus oleh mereka."
        ))
        
    elif "investment" in category or "investasi" in category:
        title = "Panduan Darurat: Penipuan Investasi"
        summary = "Hentikan pengiriman dana lebih lanjut. Jangan tergiur janji pengembalian uang (recovery scam)."
        
        steps.append(EmergencyStep(
            title="Hentikan Transfer Dana",
            description="Jangan lakukan transfer dana tambahan dengan alasan apapun, seperti 'biaya pencairan' atau 'pajak'."
        ))
        steps.append(EmergencyStep(
            title="Lapor ke OJK (Satgas PASTI)",
            description="Laporkan platform investasi bodong tersebut ke Satgas Pemberantasan Aktivitas Keuangan Ilegal (PASTI).",
            action_link="https://kontak157.ojk.go.id/"
        ))
        
        contacts.append(EmergencyContact(
            name="Kontak OJK (Satgas PASTI)",
            phone="157",
            description="Untuk melaporkan entitas investasi ilegal"
        ))
        
    else:
        title = "Panduan Darurat Umum"
        summary = "Tetap tenang dan jangan panik. Ikuti langkah-langkah dasar berikut."
        
        steps.append(EmergencyStep(
            title="Putuskan Komunikasi",
            description="Blokir nomor penipu dan jangan membalas pesan apapun dari mereka."
        ))
        steps.append(EmergencyStep(
            title="Kumpulkan Bukti",
            description="Simpan screenshot chat, nomor telepon, nomor rekening, dan URL website."
        ))
        steps.append(EmergencyStep(
            title="Laporkan ke Pihak Berwajib",
            description="Buat laporan kepolisian terdekat atau laporkan secara online."
        ))

    return EmergencyResponse(
        title=title,
        summary=summary,
        steps=steps,
        contacts=contacts
    )
