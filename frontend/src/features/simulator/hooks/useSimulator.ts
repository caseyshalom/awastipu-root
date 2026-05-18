/**
 * useSimulator — Hook untuk state management simulasi chat AI penipu.
 */

import { useState, useCallback } from 'react';
import axios from 'axios';

interface ChatMessage {
  role: 'scammer' | 'user' | 'system';
  text: string;
  redFlags?: string[];
}

interface UseSimulatorReturn {
  messages: ChatMessage[];
  tip: string;
  isRevealed: boolean;
  isLoading: boolean;
  sessionId: string | null;
  sendMessage: (text: string) => Promise<void>;
  startSession: (scenario: string) => Promise<void>;
  resetSession: () => void;
}

export default function useSimulator(): UseSimulatorReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [tip, setTip] = useState('');
  const [isRevealed, setIsRevealed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const startSession = useCallback(async (scenario: string) => {
    setIsLoading(true);
    setMessages([]);
    setIsRevealed(false);
    setTip('');

    try {
      const { data } = await axios.post('/api/v1/simulate/start', { scenario });
      setSessionId(data.session_id);
      setMessages([
        { role: 'scammer', text: data.scammer_message, redFlags: data.red_flags },
      ]);
      setTip(data.tip);
    } catch {
      setMessages([
        { role: 'system', text: '⚠️ Gagal memulai simulasi. Coba lagi.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(async (text: string) => {
    if (!sessionId || isRevealed) return;

    setMessages((prev) => [...prev, { role: 'user', text }]);
    setIsLoading(true);

    try {
      const { data } = await axios.post('/api/v1/simulate/message', {
        session_id: sessionId,
        user_message: text,
        scenario: 'phishing',
      });

      setMessages((prev) => [
        ...prev,
        { role: 'scammer', text: data.scammer_message, redFlags: data.red_flags },
      ]);
      setTip(data.tip);
      setIsRevealed(data.is_reveal);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'system', text: '⚠️ Koneksi terputus. Coba lagi.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, isRevealed]);

  const resetSession = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    setIsRevealed(false);
    setTip('');
  }, []);

  return { messages, tip, isRevealed, isLoading, sessionId, sendMessage, startSession, resetSession };
}
