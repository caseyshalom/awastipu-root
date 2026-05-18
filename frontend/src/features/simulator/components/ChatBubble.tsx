/**
 * ChatBubble — Komponen bubble chat mirip WhatsApp.
 */


interface ChatBubbleProps {
  message: string;
  sender: 'scammer' | 'user' | 'system';
  timestamp?: string;
  redFlags?: string[];
}

export default function ChatBubble({ message, sender, timestamp, redFlags }: ChatBubbleProps) {
  return (
    <div className={`chat-bubble chat-bubble-${sender}`}>
      <div className="chat-bubble-content">
        <p className="chat-bubble-text">{message}</p>
        {timestamp && <span className="chat-bubble-time">{timestamp}</span>}
      </div>
      {redFlags && redFlags.length > 0 && (
        <div className="chat-bubble-flags">
          {redFlags.map((flag, i) => (
            <span key={i} className="chat-flag">🚩 {flag}</span>
          ))}
        </div>
      )}
    </div>
  );
}
