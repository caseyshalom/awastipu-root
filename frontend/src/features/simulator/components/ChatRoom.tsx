/**
 * ChatRoom — Mockup ruang chat WhatsApp untuk simulasi penipuan.
 */

import React, { useState, useRef, useEffect } from 'react';
import ChatBubble from './ChatBubble';
import AlertBox from './AlertBox';
import { Button } from '@/components/ui';
import useSimulator from '../hooks/useSimulator';

interface ChatRoomProps {
  scenario: string;
}

export default function ChatRoom({ scenario }: ChatRoomProps) {
  const { messages, tip, isRevealed, isLoading, sendMessage, startSession } = useSimulator();
  const [inputText, setInputText] = useState('');
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    startSession(scenario);
  }, [scenario]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (inputText.trim() && !isRevealed) {
      sendMessage(inputText.trim());
      setInputText('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-room" id="chat-room">
      {/* Chat Header */}
      <div className="chat-room-header">
        <div className="chat-room-avatar">🎭</div>
        <div className="chat-room-info">
          <span className="chat-room-name">Penipu (Simulasi AI)</span>
          <span className="chat-room-status">
            {isLoading ? 'mengetik...' : 'online'}
          </span>
        </div>
        <span className="chat-room-badge">🔒 Mode Edukasi</span>
      </div>

      {/* Chat Messages */}
      <div className="chat-room-messages" ref={chatContainerRef}>
        {messages.map((msg, i) => (
          <ChatBubble
            key={i}
            message={msg.text}
            sender={msg.role}
            redFlags={msg.redFlags}
          />
        ))}
      </div>

      {/* Tip Box */}
      {tip && <AlertBox message={tip} type="tip" />}

      {/* Reveal Alert */}
      {isRevealed && (
        <AlertBox
          message="Simulasi selesai! Pelajari trik yang digunakan di atas."
          type="reveal"
        />
      )}

      {/* Input Area */}
      <div className="chat-room-input">
        <input
          type="text"
          className="chat-input-field"
          id="chat-input"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isRevealed ? 'Simulasi selesai' : 'Ketik balasan Anda...'}
          disabled={isRevealed || isLoading}
        />
        <Button
          variant="primary"
          size="sm"
          onClick={handleSend}
          disabled={isRevealed || isLoading || !inputText.trim()}
          id="chat-send-btn"
        >
          Kirim
        </Button>
      </div>
    </div>
  );
}
