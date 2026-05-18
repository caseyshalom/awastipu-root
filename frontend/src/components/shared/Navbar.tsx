/**
 * Navbar — Navigasi utama aplikasi AwasTipu.
 */

import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const NAV_LINKS = [
  { path: '/',          label: 'Beranda',   icon: '🏠' },
  { path: '/analyzer',  label: 'Detektor',  icon: '🔍' },
  { path: '/simulator', label: 'Simulator', icon: '🎮' },
  { path: '/report',    label: 'Laporan',   icon: '📋' },
];

export default function Navbar() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="navbar" id="main-navbar">
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-brand">
          <span className="navbar-logo">🛡️</span>
          <span className="navbar-title">AwasTipu</span>
        </Link>

        {/* Desktop Links */}
        <ul className="navbar-links">
          {NAV_LINKS.map((link) => (
            <li key={link.path}>
              <Link
                to={link.path}
                className={`navbar-link ${location.pathname === link.path ? 'navbar-link-active' : ''}`}
              >
                <span className="navbar-link-icon">{link.icon}</span>
                {link.label}
              </Link>
            </li>
          ))}
        </ul>

        {/* Mobile Toggle */}
        <button
          className="navbar-toggle"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle navigation"
          id="navbar-toggle-btn"
        >
          <span className={`hamburger ${mobileOpen ? 'hamburger-open' : ''}`} />
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="navbar-mobile" id="navbar-mobile-menu">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`navbar-mobile-link ${location.pathname === link.path ? 'navbar-link-active' : ''}`}
              onClick={() => setMobileOpen(false)}
            >
              <span>{link.icon}</span>
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
