/**
 * ReportPage — Halaman Database Laporan Penipuan.
 */

import { useState } from 'react';
import { Layout } from '@/components/shared';
import { ReportForm, NumberSearch } from '@/features/report/components';
import type { ReportFormData } from '@/features/report/components/ReportForm';
import axios from 'axios';

export default function ReportPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activeTab, setActiveTab] = useState<'search' | 'report'>('search');

  const handleSubmitReport = async (formData: ReportFormData) => {
    setIsSubmitting(true);
    try {
      await axios.post('/api/v1/reports/', formData);
      alert('Laporan berhasil dikirim dan tersimpan di database.');
      setActiveTab('search');
    } catch (err) {
      alert('Gagal mengirim laporan. Coba lagi.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout>
      <section className="page-section" id="report-page">
        <div className="page-header">
          <h1 className="page-title">📋 Database Laporan</h1>
          <p className="page-subtitle">
            Cek nomor penipu atau laporkan penipuan baru.
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="tab-nav" id="report-tabs">
          <button
            className={`tab-btn ${activeTab === 'search' ? 'tab-btn-active' : ''}`}
            onClick={() => setActiveTab('search')}
          >
            🔍 Cek Nomor
          </button>
          <button
            className={`tab-btn ${activeTab === 'report' ? 'tab-btn-active' : ''}`}
            onClick={() => setActiveTab('report')}
          >
            📝 Buat Laporan
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'search' && <NumberSearch />}
          {activeTab === 'report' && (
            <ReportForm onSubmit={handleSubmitReport} isLoading={isSubmitting} />
          )}
        </div>
      </section>
    </Layout>
  );
}
