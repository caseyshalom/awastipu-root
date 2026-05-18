/**
 * HomePage — Landing page utama AwasTipu.
 */


import { Link } from 'react-router-dom';
import { Layout } from '@/components/shared';
import { Button, Card } from '@/components/ui';

const FEATURES = [
  {
    icon: '🔍',
    title: 'Detektor Pesan',
    desc: 'Paste pesan mencurigakan dan dapatkan analisis instan apakah itu penipuan.',
    link: '/analyzer',
    color: '#6366f1',
  },
  {
    icon: '🎮',
    title: 'Simulator Penipuan',
    desc: 'Latihan menghadapi penipu dalam simulasi chat interaktif yang aman.',
    link: '/simulator',
    color: '#f59e0b',
  },
  {
    icon: '📋',
    title: 'Database Laporan',
    desc: 'Cek nomor telepon/rekening dan laporkan penipu ke database komunitas.',
    link: '/report',
    color: '#ef4444',
  },
];



export default function HomePage() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="hero" id="hero-section">
        <div className="hero-content">
          <span className="hero-badge" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#22c55e', display: 'inline-block', boxShadow: '0 0 8px #22c55e' }}></span>
            Online
          </span>
          <h1 className="hero-title">
            Jangan Jadi Korban <span className="text-gradient">Penipuan Online</span>
          </h1>
          <p className="hero-subtitle">
            AwasTipu menggunakan kecerdasan buatan untuk mendeteksi, mengedukasi, 
            dan melindungi masyarakat Indonesia dari modus penipuan digital.
          </p>
          <div className="hero-actions">
            <Link to="/analyzer">
              <Button variant="primary" size="lg" id="cta-analyze">
                🔍 Cek Pesan Sekarang
              </Button>
            </Link>
            <Link to="/simulator">
              <Button variant="outline" size="lg" id="cta-simulate">
                🎮 Coba Simulator
              </Button>
            </Link>
          </div>
        </div>


      </section>

      {/* Features */}
      <section className="features-section" id="features-section">
        <h2 className="section-title">Fitur Utama</h2>
        <div className="features-grid">
          {FEATURES.map((f, i) => (
            <Link to={f.link} key={i} className="feature-link">
              <Card variant="glass" padding="lg" className="feature-card">
                <span className="feature-icon" style={{ background: `${f.color}22` }}>
                  {f.icon}
                </span>
                <h3 className="feature-title">{f.title}</h3>
                <p className="feature-desc">{f.desc}</p>
                <span className="feature-arrow">→</span>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="how-section" id="how-section">
        <h2 className="section-title">Cara Kerja</h2>
        <div className="steps">
          <div className="step">
            <span className="step-number">1</span>
            <h4>Paste / Upload</h4>
            <p>Tempel pesan atau upload screenshot chat mencurigakan.</p>
          </div>
          <div className="step-divider" />
          <div className="step">
            <span className="step-number">2</span>
            <h4>AI Analisis</h4>
            <p>AI kami menganalisis pola, bahasa, dan taktik penipuan.</p>
          </div>
          <div className="step-divider" />
          <div className="step">
            <span className="step-number">3</span>
            <h4>Hasil & Saran</h4>
            <p>Dapatkan skor risiko, penjelasan, dan rekomendasi tindakan.</p>
          </div>
        </div>
      </section>
    </Layout>
  );
}
