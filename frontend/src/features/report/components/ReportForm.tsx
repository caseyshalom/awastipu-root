/**
 * ReportForm — Form untuk mengirim laporan penipuan baru.
 */

import React, { useState } from 'react';
import { Button, Input, Card } from '@/components/ui';

interface ReportFormProps {
  onSubmit: (data: ReportFormData) => Promise<void>;
  isLoading: boolean;
}

export interface ReportFormData {
  phone_number: string;
  bank_account: string;
  scam_category: string;
  description: string;
  reporter_alias: string;
}

const CATEGORIES = [
  { value: 'phishing', label: '🏦 Phishing' },
  { value: 'investment_scam', label: '📈 Investasi Bodong' },
  { value: 'romance_scam', label: '💔 Romance Scam' },
  { value: 'lottery_scam', label: '🎰 Undian Palsu' },
  { value: 'impersonation', label: '🎭 Peniruan Identitas' },
  { value: 'job_scam', label: '💼 Lowongan Palsu' },
  { value: 'shopping_scam', label: '🛒 Belanja Online' },
  { value: 'other', label: '❓ Lainnya' },
];

export default function ReportForm({ onSubmit, isLoading }: ReportFormProps) {
  const [form, setForm] = useState<ReportFormData>({
    phone_number: '',
    bank_account: '',
    scam_category: 'other',
    description: '',
    reporter_alias: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (form.description.length >= 10) {
      onSubmit(form);
    }
  };

  return (
    <Card variant="glass" padding="lg" className="report-form-card">
      <form className="report-form" onSubmit={handleSubmit} id="report-form">
        <h3>📝 Laporkan Penipuan</h3>

        <Input
          label="Nomor Telepon Penipu"
          name="phone_number"
          value={form.phone_number}
          onChange={handleChange}
          placeholder="Contoh: 081234567890"
          icon={<span>📱</span>}
        />

        <Input
          label="Nomor Rekening Penipu"
          name="bank_account"
          value={form.bank_account}
          onChange={handleChange}
          placeholder="Contoh: 1234567890"
          icon={<span>🏦</span>}
        />

        <div className="input-group">
          <label className="input-label" htmlFor="scam_category">Kategori Penipuan</label>
          <select
            id="scam_category"
            name="scam_category"
            className="input-field"
            value={form.scam_category}
            onChange={handleChange}
          >
            {CATEGORIES.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
        </div>

        <div className="input-group">
          <label className="input-label" htmlFor="description">Kronologi Kejadian *</label>
          <textarea
            id="description"
            name="description"
            className="input-field"
            value={form.description}
            onChange={handleChange}
            placeholder="Ceritakan kronologi penipuan yang Anda alami..."
            rows={4}
            required
            minLength={10}
          />
        </div>

        <Input
          label="Nama/Alias Anda"
          name="reporter_alias"
          value={form.reporter_alias}
          onChange={handleChange}
          placeholder="Anonim"
          helperText="Opsional — identitas Anda akan dilindungi"
        />

        <Button
          variant="danger"
          size="lg"
          type="submit"
          isLoading={isLoading}
          disabled={form.description.length < 10}
          id="submit-report-btn"
        >
          🚨 Kirim Laporan
        </Button>
      </form>
    </Card>
  );
}
