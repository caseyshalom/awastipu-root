/**
 * SimulatorPage — Halaman Kamar Simulasi Penipuan.
 */

import { useState, useEffect } from 'react';
import { Layout } from '@/components/shared';
import { ChatRoom, ScenarioSelector } from '@/features/simulator/components';
import axios from 'axios';

interface Scenario {
  id: string;
  name: string;
  icon: string;
}

export default function SimulatorPage() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenario, setSelectedScenario] = useState('phishing');

  useEffect(() => {
    // Load available scenarios
    axios.get('/api/v1/simulate/scenarios').then(({ data }) => {
      setScenarios(data.scenarios);
    }).catch(() => {
      // Fallback scenarios
      setScenarios([
        { id: 'phishing', name: 'Phishing', icon: '🏦' },
        { id: 'investment_scam', name: 'Investasi Bodong', icon: '📈' },
        { id: 'lottery_scam', name: 'Undian Berhadiah Palsu', icon: '🎰' },
        { id: 'romance_scam', name: 'Romance Scam', icon: '💔' },
        { id: 'job_scam', name: 'Lowongan Kerja Palsu', icon: '💼' },
      ]);
    });
  }, []);

  return (
    <Layout>
      <section className="page-section" id="simulator-page">
        <div className="page-header">
          <h1 className="page-title">🎮 Simulator Penipuan</h1>
          <p className="page-subtitle">
            Latih dirimu menghadapi penipu! Pilih skenario dan coba berinteraksi 
            dengan AI penipu dalam lingkungan yang aman.
          </p>
          <div className="page-warning">
            ⚠️ Ini adalah simulasi edukasi. Tidak ada data nyata yang digunakan.
          </div>
        </div>

        <ScenarioSelector
          scenarios={scenarios}
          selected={selectedScenario}
          onSelect={setSelectedScenario}
        />

        <ChatRoom scenario={selectedScenario} />
      </section>
    </Layout>
  );
}
