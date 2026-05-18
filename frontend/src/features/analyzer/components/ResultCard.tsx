/**
 * ResultCard — Menampilkan hasil analisis lengkap.
 */

import React from 'react';
import { Card, Badge } from '@/components/ui';

interface Tactic {
  name: string;
  description: string;
  severity: number;
}

interface AnalysisResult {
  risk_level: string;
  risk_score: number;
  category: string;
  explanation: string;
  tactics: Tactic[];
  recommendation: string;
}

interface ResultCardProps {
  result: AnalysisResult;
}

const CATEGORY_LABELS: Record<string, string> = {
  phishing: '🏦 Phishing',
  investment_scam: '📈 Investasi Bodong',
  romance_scam: '💔 Romance Scam',
  lottery_scam: '🎰 Undian Palsu',
  impersonation: '🎭 Peniruan Identitas',
  job_scam: '💼 Lowongan Palsu',
  shopping_scam: '🛒 Belanja Online Palsu',
  other: '❓ Lainnya',
};

const RISK_BADGE_VARIANT: Record<string, 'safe' | 'warning' | 'danger' | 'info'> = {
  safe: 'safe',
  low: 'safe',
  medium: 'warning',
  high: 'danger',
  critical: 'danger',
};

export default function ResultCard({ result }: ResultCardProps) {
  return (
    <Card variant="glass" padding="lg" className="result-card" id="result-card">
      {/* Header */}
      <div className="result-header">
        <Badge variant={RISK_BADGE_VARIANT[result.risk_level] || 'info'}>
          {result.risk_level.toUpperCase()}
        </Badge>
        <Badge variant="info">
          {CATEGORY_LABELS[result.category] || result.category}
        </Badge>
      </div>

      {/* Explanation */}
      <div className="result-section">
        <h4>📝 Penjelasan</h4>
        <p>{result.explanation}</p>
      </div>

      {/* Tactics */}
      {result.tactics.length > 0 && (
        <div className="result-section">
          <h4>🎯 Taktik Terdeteksi ({result.tactics.length})</h4>
          <ul className="tactic-list">
            {result.tactics.map((tactic, i) => (
              <li key={i} className="tactic-item">
                <div className="tactic-header">
                  <span className="tactic-name">{tactic.name}</span>
                  <div
                    className="tactic-severity-bar"
                    style={{ '--severity': `${tactic.severity * 100}%` } as React.CSSProperties}
                  >
                    <div className="tactic-severity-fill" />
                  </div>
                </div>
                <p className="tactic-desc">{tactic.description}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendation */}
      <div className="result-recommendation">
        <h4>💡 Rekomendasi</h4>
        <p>{result.recommendation}</p>
      </div>
    </Card>
  );
}
