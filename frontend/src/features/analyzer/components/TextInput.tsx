/**
 * TextInput — Area input teks pesan yang akan dianalisis.
 * Mendukung paste teks dan upload screenshot.
 */

import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui';

interface TextInputProps {
  onAnalyze: (text: string) => void;
  onImageUpload: (file: File) => void;
  isLoading: boolean;
}

export default function TextInput({ onAnalyze, onImageUpload, isLoading }: TextInputProps) {
  const [text, setText] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim().length >= 5) {
      onAnalyze(text.trim());
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageUpload(file);
    }
  };

  return (
    <form className="analyzer-input" onSubmit={handleSubmit} id="analyzer-form">
      <div className="analyzer-input-header">
        <h3>📩 Paste Pesan Mencurigakan</h3>
        <p className="text-muted">
          Tempel pesan SMS, WhatsApp, atau email yang ingin Anda periksa.
        </p>
      </div>

      <textarea
        className="analyzer-textarea"
        id="analyzer-textarea"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Contoh: Selamat! Anda memenangkan hadiah Rp 100juta. Klik link berikut untuk klaim..."
        rows={6}
        maxLength={5000}
        disabled={isLoading}
      />

      <div className="analyzer-input-footer">
        <span className="char-count">{text.length}/5000</span>
        <div className="analyzer-actions">
          <Button
            variant="ghost"
            size="sm"
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            icon={<span>📷</span>}
          >
            Upload Screenshot
          </Button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/webp"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <Button
            variant="primary"
            size="md"
            type="submit"
            isLoading={isLoading}
            disabled={text.trim().length < 5}
            id="analyze-btn"
          >
            🔍 Analisis Sekarang
          </Button>
        </div>
      </div>
    </form>
  );
}
