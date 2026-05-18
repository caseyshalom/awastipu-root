/**
 * Footer — Footer aplikasi AwasTipu.
 */

import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="footer" id="main-footer">
      <div className="footer-container">
        <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '2rem', marginBottom: '2rem' }}>
          <div className="footer-brand" style={{ marginBottom: 0 }}>
            <span className="footer-logo">🛡️</span>
            <p className="footer-tagline">
              AwasTipu — Lindungi dirimu dari penipuan online dengan AI.
            </p>
          </div>

          <div className="footer-links" style={{ marginBottom: 0 }}>
            <div className="footer-col">
              <h4 className="footer-col-title">Fitur</h4>
              <Link to="/analyzer">Detektor Pesan</Link>
              <Link to="/simulator">Simulator Scam</Link>
              <Link to="/report">Database Laporan</Link>
            </div>
            <div className="footer-col">
              <h4 className="footer-col-title">Info</h4>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
              <a href="#privacy">Kebijakan Privasi</a>
              <a href="#about">Tentang Kami</a>
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
