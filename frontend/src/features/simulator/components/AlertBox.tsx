/**
 * AlertBox — Box untuk tips dan reveal penipuan.
 */


interface AlertBoxProps {
  message: string;
  type: 'tip' | 'reveal' | 'warning';
}

const ICONS: Record<string, string> = {
  tip: '💡',
  reveal: '🎓',
  warning: '⚠️',
};

export default function AlertBox({ message, type }: AlertBoxProps) {
  return (
    <div className={`alert-box alert-box-${type}`}>
      <span className="alert-box-icon">{ICONS[type]}</span>
      <p className="alert-box-text">{message}</p>
    </div>
  );
}
