/**
 * VibeMeter — Meteran Gas UI untuk menampilkan skor risiko.
 * Animasi gauge yang berputar dari aman (hijau) ke bahaya (merah).
 */

import { useEffect, useState } from 'react';

interface VibeMeterProps {
  score: number;       // 0–100
  riskLevel: string;   // safe | low | medium | high | critical
  animate?: boolean;
}

const RISK_COLORS: Record<string, string> = {
  safe:     '#22c55e',
  low:      '#84cc16',
  medium:   '#f59e0b',
  high:     '#ef4444',
  critical: '#dc2626',
};

const RISK_LABELS: Record<string, string> = {
  safe:     'AMAN ✅',
  low:      'Risiko Rendah',
  medium:   'WASPADA ⚠️',
  high:     'BAHAYA! 🔴',
  critical: '🚨 SANGAT BAHAYA!',
};

export default function VibeMeter({ score, riskLevel, animate = true }: VibeMeterProps) {
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    if (!animate) {
      setDisplayScore(score);
      return;
    }

    let current = 0;
    const step = score / 60; // ~60 frames
    const interval = setInterval(() => {
      current += step;
      if (current >= score) {
        setDisplayScore(score);
        clearInterval(interval);
      } else {
        setDisplayScore(Math.round(current));
      }
    }, 16);

    return () => clearInterval(interval);
  }, [score, animate]);

  const color = RISK_COLORS[riskLevel] || RISK_COLORS.safe;
  const label = RISK_LABELS[riskLevel] || 'Tidak Diketahui';

  // SVG gauge rotation: 0 = left (-90deg), 100 = right (90deg)
  const rotation = -90 + (displayScore / 100) * 180;

  return (
    <div className="vibe-meter" id="vibe-meter">
      <svg viewBox="0 0 200 120" className="vibe-meter-svg">
        {/* Background arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="16"
          strokeLinecap="round"
        />
        {/* Colored arc (gradient stops) */}
        <defs>
          <linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#22c55e" />
            <stop offset="35%" stopColor="#f59e0b" />
            <stop offset="70%" stopColor="#ef4444" />
            <stop offset="100%" stopColor="#dc2626" />
          </linearGradient>
        </defs>
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="url(#gauge-gradient)"
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray="251"
          strokeDashoffset={251 - (displayScore / 100) * 251}
          style={{ transition: 'stroke-dashoffset 0.3s ease' }}
        />
        {/* Needle */}
        <line
          x1="100"
          y1="100"
          x2="100"
          y2="35"
          stroke={color}
          strokeWidth="3"
          strokeLinecap="round"
          transform={`rotate(${rotation}, 100, 100)`}
          style={{ transition: 'transform 0.5s ease-out' }}
        />
        {/* Center dot */}
        <circle cx="100" cy="100" r="6" fill={color} />
      </svg>

      <div className="vibe-meter-info">
        <span className="vibe-meter-score" style={{ color }}>
          {displayScore}
        </span>
        <span className="vibe-meter-label" style={{ color }}>
          {label}
        </span>
      </div>
    </div>
  );
}
