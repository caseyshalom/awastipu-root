/**
 * useAnalyzer — Hook untuk logika analisis pesan.
 */

import { useState, useCallback } from 'react';
import { analyzeText, analyzeImage, AnalyzeResult } from '../services/analyzerService';

interface UseAnalyzerReturn {
  result: AnalyzeResult | null;
  isLoading: boolean;
  error: string | null;
  analyze: (text: string) => Promise<void>;
  uploadAndAnalyze: (file: File) => Promise<void>;
  reset: () => void;
}

export default function useAnalyzer(): UseAnalyzerReturn {
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = useCallback(async (text: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeText(text);
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal menganalisis teks. Coba lagi.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const uploadAndAnalyze = useCallback(async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeImage(file);
      setResult(data.analysis);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal menganalisis gambar. Coba lagi.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return { result, isLoading, error, analyze, uploadAndAnalyze, reset };
}
