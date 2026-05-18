/**
 * AnalyzerPage — Halaman fitur Detektor Pesan & Vibe Meter.
 */


import { Layout } from '@/components/shared';
import { TextInput, VibeMeter, ResultCard } from '@/features/analyzer/components';
import useAnalyzer from '@/features/analyzer/hooks/useAnalyzer';

export default function AnalyzerPage() {
  const { result, isLoading, error, analyze, uploadAndAnalyze, reset } = useAnalyzer();

  return (
    <Layout>
      <section className="page-section" id="analyzer-page">
        <div className="page-header">
          <h1 className="page-title">🔍 Detektor Pesan</h1>
          <p className="page-subtitle">
            Paste pesan mencurigakan atau upload screenshot untuk dianalisis oleh AI.
          </p>
        </div>

        <div className="analyzer-layout">
          {/* Input Column */}
          <div className="analyzer-col">
            <TextInput
              onAnalyze={analyze}
              onImageUpload={uploadAndAnalyze}
              isLoading={isLoading}
            />
          </div>

          {/* Result Column */}
          <div className="analyzer-col">
            {error && (
              <div className="error-box">
                <p>❌ {error}</p>
                <button onClick={reset} className="error-retry">Coba Lagi</button>
              </div>
            )}

            {result && (
              <>
                <VibeMeter
                  score={result.risk_score}
                  riskLevel={result.risk_level}
                />
                <ResultCard result={result} />
              </>
            )}

            {!result && !error && !isLoading && (
              <div className="analyzer-placeholder">
                <span className="placeholder-icon">🛡️</span>
                <p>Hasil analisis akan muncul di sini</p>
              </div>
            )}
          </div>
        </div>
      </section>
    </Layout>
  );
}
