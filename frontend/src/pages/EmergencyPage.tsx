import { useState } from 'react';
import { Layout } from '@/components/shared';
import { Card, Button } from '@/components/ui';

// Tipografi modern dan warna akan mengikuti globals.css
// Gunakan glassmorphism dan micro-animations untuk hasil yang premium

interface EmergencyStep {
  title: string;
  description: string;
  action_link?: string;
}

interface EmergencyContact {
  name: string;
  phone: string;
  description?: string;
}

interface EmergencyResponse {
  title: string;
  summary: string;
  steps: EmergencyStep[];
  contacts: EmergencyContact[];
}

export default function EmergencyPage() {
  const [step, setStep] = useState(1);
  const [category, setCategory] = useState('');
  const [isCustomCategory, setIsCustomCategory] = useState(false);
  const [lostItem, setLostItem] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EmergencyResponse | null>(null);

  const handleNext = () => setStep(step + 1);
  const handleBack = () => setStep(step - 1);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/emergency/guide', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ scam_category: category, lost_item: lostItem }),
      });
      const data = await res.json();
      setResult(data);
      setStep(3);
    } catch (error: any) {
      console.error(error);
      alert("Terjadi kesalahan atau server tidak merespon: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setStep(1);
    setCategory('');
    setIsCustomCategory(false);
    setLostItem('');
    setResult(null);
  };

  return (
    <Layout>
      <div 
        style={{
          minHeight: '80vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem 1rem',
          position: 'relative'
        }}
      >
        <div 
          style={{
            position: 'absolute',
            top: '-10%',
            left: '-10%',
            width: '400px',
            height: '400px',
            background: 'radial-gradient(circle, rgba(239, 68, 68, 0.15) 0%, transparent 70%)',
            filter: 'blur(40px)',
            zIndex: 0
          }}
        />

        <Card 
          variant="glass" 
          padding="lg"
          style={{ 
            maxWidth: '600px', 
            width: '100%', 
            zIndex: 1,
            position: 'relative',
            border: '1px solid rgba(239, 68, 68, 0.2)',
            boxShadow: '0 8px 32px rgba(239, 68, 68, 0.1)'
          }}
        >
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <span style={{ fontSize: '3rem', display: 'block', marginBottom: '1rem', animation: 'pulse 2s infinite' }}>🚨</span>
            <h1 className="text-gradient" style={{ fontSize: '2rem', marginBottom: '0.5rem', background: 'linear-gradient(90deg, #ef4444, #f97316)', WebkitBackgroundClip: 'text', color: 'transparent' }}>
              Pusat Bantuan Darurat
            </h1>
            <p style={{ color: 'var(--text-secondary)' }}>
              Jangan panik. Kami akan memandu Anda langkah demi langkah.
            </p>
          </div>

          {/* Stepper Content */}
          <div style={{ minHeight: '300px', display: 'flex', flexDirection: 'column' }}>
            {step === 1 && (
              <div style={{ animation: 'fadeIn 0.5s ease-out' }}>
                <h3 style={{ marginBottom: '1.5rem', color: 'var(--text-primary)' }}>Apa jenis penipuan yang terjadi?</h3>
                <div style={{ display: 'grid', gap: '1rem' }}>
                  {['Phishing / Link Palsu', 'Investasi Bodong', 'Penipuan Belanja', 'Akun Diretas / Diambil Alih', 'Lainnya'].map((cat) => {
                    const isActive = category === cat || (cat === 'Lainnya' && isCustomCategory);
                    return (
                    <Button 
                      key={cat}
                      variant={isActive ? 'primary' : 'outline'}
                      style={{ 
                        justifyContent: 'flex-start', 
                        padding: '1rem',
                        borderColor: isActive ? '#ef4444' : 'rgba(255,255,255,0.1)',
                        background: isActive ? 'linear-gradient(90deg, #ef4444, #dc2626)' : 'transparent'
                      }}
                      onClick={() => {
                        if (cat === 'Lainnya') {
                          setIsCustomCategory(true);
                          if (['Phishing / Link Palsu', 'Investasi Bodong', 'Penipuan Belanja', 'Akun Diretas / Diambil Alih'].includes(category)) {
                            setCategory('');
                          }
                        } else {
                          setIsCustomCategory(false);
                          setCategory(cat);
                          setTimeout(handleNext, 300);
                        }
                      }}
                    >
                      {cat}
                    </Button>
                  )})}
                </div>
                {isCustomCategory && (
                  <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', animation: 'fadeIn 0.3s ease-out' }}>
                    <input 
                      type="text" 
                      value={category}
                      onChange={(e) => setCategory(e.target.value)}
                      placeholder="Ketik jenis penipuan..."
                      style={{ 
                        flex: 1, 
                        padding: '0.75rem 1rem', 
                        borderRadius: '8px', 
                        border: '1px solid rgba(239, 68, 68, 0.4)', 
                        background: 'rgba(0,0,0,0.2)', 
                        color: 'white',
                        outline: 'none'
                      }}
                      autoFocus
                    />
                    <Button variant="primary" onClick={handleNext} disabled={!category.trim()}>Lanjut</Button>
                  </div>
                )}
              </div>
            )}

            {step === 2 && (
              <div style={{ animation: 'fadeIn 0.5s ease-out' }}>
                <h3 style={{ marginBottom: '1.5rem', color: 'var(--text-primary)' }}>Apa yang hilang atau terdampak?</h3>
                <div style={{ display: 'grid', gap: '1rem' }}>
                  {['Uang (Transfer/Saldo)', 'Data Pribadi (KTP/Foto)', 'Akses Akun (Medsos/Bank)', 'Tidak Ada (Hanya Terancam)'].map((item) => (
                    <Button 
                      key={item}
                      variant={lostItem === item ? 'primary' : 'outline'}
                      style={{ 
                        justifyContent: 'flex-start', 
                        padding: '1rem',
                        borderColor: lostItem === item ? '#f59e0b' : 'rgba(255,255,255,0.1)',
                        background: lostItem === item ? 'linear-gradient(90deg, #f59e0b, #d97706)' : 'transparent'
                      }}
                      onClick={() => setLostItem(item)}
                    >
                      {item}
                    </Button>
                  ))}
                </div>
                
                <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
                  <Button variant="outline" onClick={handleBack} style={{ flex: 1 }}>Kembali</Button>
                  <Button 
                    variant="primary" 
                    onClick={handleSubmit} 
                    disabled={!lostItem || loading}
                    style={{ flex: 2, background: 'linear-gradient(90deg, #ef4444, #dc2626)' }}
                  >
                    {loading ? 'Memproses...' : 'Dapatkan Panduan'}
                  </Button>
                </div>
              </div>
            )}

            {step === 3 && result && (
              <div style={{ animation: 'fadeIn 0.5s ease-out', flex: 1, display: 'flex', flexDirection: 'column' }}>
                <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', borderLeft: '4px solid #ef4444', marginBottom: '2rem' }}>
                  <h3 style={{ color: '#ef4444', marginBottom: '0.5rem' }}>{result.title}</h3>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{result.summary}</p>
                </div>

                <div style={{ marginBottom: '2rem' }}>
                  <h4 style={{ marginBottom: '1rem', color: 'var(--text-primary)' }}>Langkah Darurat:</h4>
                  <div style={{ display: 'grid', gap: '1rem' }}>
                    {result.steps.map((s, i) => (
                      <div key={i} style={{ 
                        display: 'flex', 
                        gap: '1rem',
                        background: 'rgba(255,255,255,0.03)',
                        padding: '1rem',
                        borderRadius: '12px',
                        border: '1px solid rgba(255,255,255,0.05)'
                      }}>
                        <div style={{ 
                          width: '24px', 
                          height: '24px', 
                          borderRadius: '50%', 
                          background: '#ef4444', 
                          color: 'white', 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'center', 
                          fontSize: '0.8rem',
                          fontWeight: 'bold',
                          flexShrink: 0
                        }}>
                          {i + 1}
                        </div>
                        <div>
                          <h5 style={{ marginBottom: '0.25rem', color: 'var(--text-primary)' }}>{s.title}</h5>
                          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{s.description}</p>
                          {s.action_link && (
                            <a 
                              href={s.action_link} 
                              style={{ 
                                display: 'inline-block', 
                                marginTop: '0.5rem', 
                                fontSize: '0.85rem', 
                                color: '#3b82f6',
                                textDecoration: 'none'
                              }}
                            >
                              Buka Link →
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div style={{ marginBottom: '2rem' }}>
                  <h4 style={{ marginBottom: '1rem', color: 'var(--text-primary)' }}>Kontak Penting:</h4>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    {result.contacts.map((c, i) => (
                      <div key={i} style={{ 
                        background: 'rgba(59, 130, 246, 0.1)',
                        padding: '1rem',
                        borderRadius: '12px',
                        border: '1px solid rgba(59, 130, 246, 0.2)'
                      }}>
                        <h5 style={{ color: '#60a5fa', marginBottom: '0.25rem' }}>{c.name}</h5>
                        <p style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--text-primary)', marginBottom: '0.25rem' }}>{c.phone}</p>
                        {c.description && <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{c.description}</p>}
                      </div>
                    ))}
                  </div>
                </div>

                <div style={{ marginTop: 'auto', textAlign: 'center' }}>
                  <Button variant="outline" onClick={resetForm}>Konsultasi Ulang</Button>
                </div>
              </div>
            )}
          </div>
        </Card>
      </div>
    </Layout>
  );
}
