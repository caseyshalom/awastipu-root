/**
 * NumberSearch — Cari nomor telepon/rekening di database laporan.
 */

import { useState } from 'react';
import { Button, Input, Card, Badge } from '@/components/ui';
import axios from 'axios';

interface SearchResult {
  found: boolean;
  count: number;
  message: string;
  results: any[];
}

export default function NumberSearch() {
  const [phone, setPhone] = useState('');
  const [account, setAccount] = useState('');
  const [result, setResult] = useState<SearchResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    if (!phone && !account) return;
    setIsLoading(true);

    try {
      const params = new URLSearchParams();
      if (phone) params.append('phone', phone);
      if (account) params.append('account', account);

      const { data } = await axios.get(`/api/v1/reports/search?${params}`);
      setResult(data);
    } catch {
      setResult({ found: false, count: 0, message: 'Gagal mencari. Coba lagi.', results: [] });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card variant="glass" padding="lg" className="number-search" id="number-search">
      <h3>🔍 Cek Nomor Penipu</h3>
      <p className="text-muted">Verifikasi nomor telepon atau rekening sebelum bertransaksi.</p>

      <div className="search-inputs">
        <Input
          label="Nomor Telepon"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="081234567890"
          icon={<span>📱</span>}
        />
        <Input
          label="Nomor Rekening"
          value={account}
          onChange={(e) => setAccount(e.target.value)}
          placeholder="1234567890"
          icon={<span>🏦</span>}
        />
      </div>

      <Button
        variant="primary"
        onClick={handleSearch}
        isLoading={isLoading}
        disabled={!phone && !account}
        id="search-number-btn"
      >
        Cari Sekarang
      </Button>

      {result && (
        <div className={`search-result ${result.found ? 'search-result-found' : 'search-result-safe'}`}>
          <Badge variant={result.found ? 'danger' : 'safe'}>
            {result.found ? '⚠️ DITEMUKAN' : '✅ TIDAK DITEMUKAN'}
          </Badge>
          <p>{result.message}</p>
        </div>
      )}
    </Card>
  );
}
