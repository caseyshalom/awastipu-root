import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AnalyzerPage from './pages/AnalyzerPage';
import SimulatorPage from './pages/SimulatorPage';
import EmergencyPage from './pages/EmergencyPage';
import NotFoundPage from './pages/NotFoundPage';

export default function App() {
  return (
    <Routes>
      <Route path="/"           element={<HomePage />} />
      <Route path="/analyzer"   element={<AnalyzerPage />} />
      <Route path="/simulator"  element={<SimulatorPage />} />
      <Route path="/emergency"  element={<EmergencyPage />} />
      <Route path="*"           element={<NotFoundPage />} />
    </Routes>
  );
}
