/**
 * analyzerService — API calls untuk fitur analisis teks/gambar.
 */

import axios from 'axios';

const API_BASE = '/api/v1/analyze';

export interface AnalyzeResult {
  risk_level: string;
  risk_score: number;
  category: string;
  explanation: string;
  tactics: { name: string; description: string; severity: number }[];
  recommendation: string;
}

/**
 * Analisis teks pesan.
 */
export async function analyzeText(text: string, includeTactics = true): Promise<AnalyzeResult> {
  const { data } = await axios.post<AnalyzeResult>(`${API_BASE}/text`, {
    text,
    include_tactics: includeTactics,
  });
  return data;
}

/**
 * Upload & analisis screenshot.
 */
export async function analyzeImage(file: File): Promise<{
  extracted_text: string;
  analysis: AnalyzeResult;
}> {
  const formData = new FormData();
  formData.append('file', file);

  const { data } = await axios.post(`${API_BASE}/image`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}
