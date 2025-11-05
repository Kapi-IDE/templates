import React from 'react';
import ResearchInterface from './components/ResearchInterface';
import PortfolioDashboard from './components/PortfolioDashboard';
import RiskAnalysis from './components/RiskAnalysis';
import ReportGenerator from './components/ReportGenerator';
import ComplianceMonitor from './components/ComplianceMonitor';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Investment Research Platform</h1>
      </header>
      <main>
        <ResearchInterface />
        <PortfolioDashboard />
        <RiskAnalysis />
        <ReportGenerator />
        <ComplianceMonitor />
      </main>
    </div>
  );
}

export default App;
