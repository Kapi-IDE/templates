import React, { useEffect, useState } from 'react';
import './App.css';
import { getHealth } from './services/api';
import LegalResearchPanel from './components/LegalResearchPanel';
import DocumentAnalysisPanel from './components/DocumentAnalysisPanel';
import CaseManagementPanel from './components/CaseManagementPanel';
import PrivilegedChatPanel from './components/PrivilegedChatPanel';
import EthicsDashboard from './components/EthicsDashboard';

const tabs = [
  { id: 'research', label: 'Research' },
  { id: 'documents', label: 'Documents' },
  { id: 'cases', label: 'Cases' },
  { id: 'chat', label: 'Privileged Chat' },
  { id: 'ethics', label: 'Ethics' },
];

function App() {
  const [activeTab, setActiveTab] = useState('research');
  const [attorneyId, setAttorneyId] = useState('attorney-1');
  const [clientId, setClientId] = useState('client-1');
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const status = await getHealth();
        setHealth(status);
      } catch (error) {
        setHealth({ status: 'degraded', error: error.message });
      }
    };
    fetchHealth();
  }, []);

  const renderActivePanel = () => {
    switch (activeTab) {
      case 'research':
        return <LegalResearchPanel attorneyId={attorneyId} clientId={clientId} />;
      case 'documents':
        return <DocumentAnalysisPanel attorneyId={attorneyId} clientId={clientId} caseId={selectedCaseId} />;
      case 'cases':
        return <CaseManagementPanel attorneyId={attorneyId} onCaseSelected={setSelectedCaseId} />;
      case 'chat':
        return <PrivilegedChatPanel attorneyId={attorneyId} clientId={clientId} />;
      case 'ethics':
        return <EthicsDashboard attorneyId={attorneyId} />;
      default:
        return null;
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Legal Analysis Blueprint</h1>
          <p className="muted">Multi-agent legal intelligence with privilege safeguards</p>
        </div>
        <div className="identity-controls">
          <label>
            Attorney ID
            <input value={attorneyId} onChange={(event) => setAttorneyId(event.target.value)} />
          </label>
          <label>
            Client ID
            <input value={clientId} onChange={(event) => setClientId(event.target.value)} />
          </label>
          {health && (
            <span className={`status-badge status-badge--${health.status || 'unknown'}`}>
              {health.status || 'unknown'}
            </span>
          )}
        </div>
      </header>

      <nav className="tab-nav">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={tab.id === activeTab ? 'active' : ''}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="app-main">{renderActivePanel()}</main>
    </div>
  );
}

export default App;
