/**
 * Footer — Footer aplikasi AwasTipu.
 */

import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="footer" id="main-footer" style={{ borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '3rem', marginTop: 'auto' }}>
      <div className="footer-container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem 3rem' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', gap: '3rem', marginBottom: '3rem' }}>
          
          {/* Kolom 1: Brand & Misi */}
          <div className="footer-brand" style={{ marginBottom: 0, flex: '1 1 400px', maxWidth: '600px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <span className="footer-logo" style={{ fontSize: '1.8rem', background: 'rgba(59, 130, 246, 0.2)', padding: '0.5rem', borderRadius: '12px' }}>🛡️</span>
              <h3 style={{ fontSize: '1.6rem', fontWeight: '800', margin: 0, background: 'linear-gradient(to right, #60a5fa 0%, #3b82f6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', letterSpacing: '-0.5px' }}>
                AwasTipu
              </h3>
            </div>
            <p className="footer-tagline" style={{ color: '#9ca3af', lineHeight: '1.7', fontSize: '0.95rem', margin: 0, fontStyle: 'italic' }}>
              Platform cerdas berbasis AI untuk mendeteksi, mencegah, dan mengedukasi masyarakat Indonesia dari ancaman penipuan digital. Mari bersama menciptakan ruang siber yang lebih aman dan terpercaya.
            </p>
          </div>

          {/* Kolom 2: Layanan Utama */}
          <div className="footer-col" style={{ display: 'flex', flexDirection: 'column' }}>
            <h4 className="footer-col-title" style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '1.25rem', color: '#f3f4f6', letterSpacing: '0.5px' }}>Layanan Utama</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <Link to="/analyzer" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'all 0.2s ease', display: 'flex', alignItems: 'center', gap: '0.5rem' }} onMouseOver={(e) => { e.currentTarget.style.color = '#60a5fa'; e.currentTarget.style.transform = 'translateX(5px)'; }} onMouseOut={(e) => { e.currentTarget.style.color = '#9ca3af'; e.currentTarget.style.transform = 'translateX(0)'; }}>
                <span>🔍</span> Detektor Pesan
              </Link>
              <Link to="/simulator" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'all 0.2s ease', display: 'flex', alignItems: 'center', gap: '0.5rem' }} onMouseOver={(e) => { e.currentTarget.style.color = '#60a5fa'; e.currentTarget.style.transform = 'translateX(5px)'; }} onMouseOut={(e) => { e.currentTarget.style.color = '#9ca3af'; e.currentTarget.style.transform = 'translateX(0)'; }}>
                <span>🎮</span> Simulator Scam
              </Link>
              <Link to="/report" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'all 0.2s ease', display: 'flex', alignItems: 'center', gap: '0.5rem' }} onMouseOver={(e) => { e.currentTarget.style.color = '#60a5fa'; e.currentTarget.style.transform = 'translateX(5px)'; }} onMouseOut={(e) => { e.currentTarget.style.color = '#9ca3af'; e.currentTarget.style.transform = 'translateX(0)'; }}>
                <span>📋</span> Database Laporan
              </Link>
            </div>
          </div>
          
        </div>

        <div className="footer-bottom">
          <p>Copyright &copy; 2026 AwasTipu | All Rights Reserved</p>
        </div>
      </div>
    </footer>
  );
}
