/**
 * ScenarioSelector — Pilihan skenario penipuan untuk simulasi.
 */

import { Card } from '@/components/ui';

interface Scenario {
  id: string;
  name: string;
  icon: string;
}

interface ScenarioSelectorProps {
  scenarios: Scenario[];
  selected: string;
  onSelect: (id: string) => void;
}

export default function ScenarioSelector({ scenarios, selected, onSelect }: ScenarioSelectorProps) {
  return (
    <div className="scenario-selector" id="scenario-selector">
      <h3 className="scenario-title">Pilih Skenario Penipuan</h3>
      <div className="scenario-grid">
        {scenarios.map((s) => (
          <Card
            key={s.id}
            variant={selected === s.id ? 'elevated' : 'glass'}
            padding="sm"
            className={`scenario-card ${selected === s.id ? 'scenario-card-active' : ''}`}
            onClick={() => onSelect(s.id)}
          >
            <span className="scenario-icon">{s.icon}</span>
            <span className="scenario-name">{s.name}</span>
          </Card>
        ))}
      </div>
    </div>
  );
}
