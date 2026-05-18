/**
 * ReportPage — Halaman Database Laporan Penipuan.
 */

import { useState, useEffect, useCallback } from 'react';
import { Layout } from '@/components/shared';
import { ReportForm, ReportList, NumberSearch } from '@/features/report/components';
import type { ReportFormData } from '@/features/report/components/ReportForm';
import axios from 'axios';

export default function ReportPage() {
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activeTab, setActiveTab] = useState<'search' | 'report' | 'list'>('search');

  const loadReports = useCallback(async () => {
    setIsLoading(true);
    try {
      const { data } = await axios.get('/api/v1/reports/?limit=20');
      setReports(data);
    } catch {
      setReports([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadReports();
  }, [loadReports]);

  const handleSubmitReport = async (formData: ReportFormData) => {
    setIsSubmitting(true);
    try {
      await axios.post('/api/v1/reports/', formData);
      setActiveTab('list');
      await loadReports();
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
            Cek nomor penipu, lihat laporan masyarakat, atau laporkan penipuan baru.
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
          <button
            className={`tab-btn ${activeTab === 'list' ? 'tab-btn-active' : ''}`}
            onClick={() => setActiveTab('list')}
          >
            📋 Daftar Laporan
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'search' && <NumberSearch />}
          {activeTab === 'report' && (
            <ReportForm onSubmit={handleSubmitReport} isLoading={isSubmitting} />
          )}
          {activeTab === 'list' && (
            <ReportList reports={reports} isLoading={isLoading} />
          )}
        </div>
      </section>
    </Layout>
  );
}
