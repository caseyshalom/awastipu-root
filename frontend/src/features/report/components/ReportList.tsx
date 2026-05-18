/**
 * ReportList — Daftar laporan penipuan dari masyarakat.
 */


import { Card, Badge } from '@/components/ui';

interface Report {
  id: number;
  phone_number?: string;
  bank_account?: string;
  scam_category: string;
  description: string;
  reporter_alias: string;
  risk_score: number;
  report_count: number;
  created_at: string;
}

interface ReportListProps {
  reports: Report[];
  isLoading: boolean;
}

const CATEGORY_LABELS: Record<string, string> = {
  phishing: '🏦 Phishing',
  investment_scam: '📈 Investasi',
  romance_scam: '💔 Romance',
  lottery_scam: '🎰 Undian',
  impersonation: '🎭 Peniruan',
  job_scam: '💼 Kerja',
  shopping_scam: '🛒 Belanja',
  other: '❓ Lainnya',
};

export default function ReportList({ reports, isLoading }: ReportListProps) {
  if (isLoading) {
    return (
      <div className="report-list-loading">
        <div className="spinner" />
        <p>Memuat laporan...</p>
      </div>
    );
  }

  if (reports.length === 0) {
    return (
      <div className="report-list-empty">
        <p>📭 Belum ada laporan. Jadilah yang pertama melaporkan!</p>
      </div>
    );
  }

  return (
    <div className="report-list" id="report-list">
      {reports.map((report) => (
        <Card key={report.id} variant="glass" padding="md" className="report-item">
          <div className="report-item-header">
            <Badge variant={report.risk_score >= 50 ? 'danger' : 'warning'}>
              Skor: {report.risk_score}
            </Badge>
            <Badge variant="info">
              {CATEGORY_LABELS[report.scam_category] || report.scam_category}
            </Badge>
            <span className="report-count">
              📢 {report.report_count}x dilaporkan
            </span>
          </div>

          <div className="report-item-body">
            {report.phone_number && (
              <p className="report-number">📱 {report.phone_number}</p>
            )}
            {report.bank_account && (
              <p className="report-number">🏦 {report.bank_account}</p>
            )}
            <p className="report-desc">{report.description.slice(0, 200)}...</p>
          </div>

          <div className="report-item-footer">
            <span className="report-alias">oleh {report.reporter_alias}</span>
            <span className="report-date">
              {new Date(report.created_at).toLocaleDateString('id-ID')}
            </span>
          </div>
        </Card>
      ))}
    </div>
  );
}
