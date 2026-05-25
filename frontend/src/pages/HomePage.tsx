import { useEffect, useRef } from 'react';
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
    icon: '🚑',
    title: 'Pusat Bantuan Darurat',
    desc: 'Panduan langkah demi langkah jika Anda sudah terlanjur menjadi korban penipuan.',
    link: '/emergency',
    color: '#ef4444',
  },
];

// Canvas-based Plexus Cyber Network background animation (clean, elegant, and eye-friendly)
function ScamMatrixBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let width = (canvas.width = canvas.parentElement?.offsetWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.offsetHeight || 400);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = canvas.parentElement?.offsetWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement?.offsetHeight || 400;
    };

    window.addEventListener('resize', handleResize);

    // Particle class definition
    interface Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
    }

    const particles: Particle[] = [];
    const particleCount = Math.min(40, Math.floor(width / 30)); // Scale with width, keep it tidy
    const connectionDistance = 100;

    // Initialize particles
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.4, // Very slow motion
        vy: (Math.random() - 0.5) * 0.4,
        radius: Math.random() * 2 + 1.5,
      });
    }

    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      // Update and draw particles
      particles.forEach((p) => {
        p.x += p.vx;
        p.y += p.vy;

        // Bounce off walls gently
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        // Draw particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(99, 102, 241, 0.25)'; // Soft indigo glow
        ctx.fill();
      });

      // Draw connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const p1 = particles[i];
          const p2 = particles[j];

          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < connectionDistance) {
            // Faint line based on distance (closer = slightly more visible)
            const alpha = (1 - dist / connectionDistance) * 0.12;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }

      animationId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 1,
        pointerEvents: 'none',
      }}
    />
  );
}

export default function HomePage() {
  return (
    <Layout>
      {/* Hero Section */}
      <section 
        className="hero" 
        id="hero-section" 
        style={{ 
          position: 'relative', 
          overflow: 'hidden', 
          borderRadius: '16px',
          background: 'linear-gradient(135deg, rgba(18, 18, 42, 0.8) 0%, rgba(10, 10, 26, 0.95) 100%)',
          border: '1px solid rgba(255, 255, 255, 0.05)',
          padding: '5rem 1rem 4rem',
          boxShadow: 'inset 0 0 40px rgba(99, 102, 241, 0.1)'
        }}
      >
        {/* Animated Scam Matrix Background */}
        <ScamMatrixBackground />

        {/* Hero Content with overlay layer */}
        <div className="hero-content" style={{ position: 'relative', zIndex: 2 }}>
          <span className="hero-badge" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#22c55e', display: 'inline-block', boxShadow: '0 0 8px #22c55e' }}></span>
            Online
          </span>
          <h1 className="hero-title" style={{ position: 'relative' }}>
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
