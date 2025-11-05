import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import Card from './Card';
import { analyzeCase, createCase, listCases } from '../services/api';

const initialCaseForm = {
  caseTitle: '',
  caseType: 'litigation',
  jurisdiction: '',
  clientId: '',
};

const CaseManagementPanel = ({ attorneyId, onCaseSelected }) => {
  const [caseForm, setCaseForm] = useState(initialCaseForm);
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [analysisIssues, setAnalysisIssues] = useState(['breach of contract']);

  const loadCases = async () => {
    setLoading(true);
    try {
      const response = await listCases({ attorneyId });
      setCases(response.cases || []);
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCases();
  }, [attorneyId]);

  const handleCreateCase = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await createCase({
        ...caseForm,
        attorneyId,
      });
      setCaseForm(initialCaseForm);
      await loadCases();
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyseCase = async () => {
    if (!selectedCaseId) return;
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeCase(selectedCaseId, {
        caseOverview: `Analysis for ${selectedCaseId}`,
        legalIssues: analysisIssues.filter(Boolean),
        attorneyId,
      });
      setAnalysis(result);
      if (onCaseSelected) {
        onCaseSelected(selectedCaseId);
      }
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      title="Case Management"
      subtitle="Track matters, run strategic analysis, and sync with AI agents"
    >
      {error && <div className="alert alert--error">{error}</div>}
      <div className="grid cols-2">
        <div>
          <h3>Create Case</h3>
          <form className="stack" onSubmit={handleCreateCase}>
            <label>
              Case Title
              <input
                required
                value={caseForm.caseTitle}
                onChange={(event) => setCaseForm({ ...caseForm, caseTitle: event.target.value })}
              />
            </label>
            <label>
              Case Type
              <select
                value={caseForm.caseType}
                onChange={(event) => setCaseForm({ ...caseForm, caseType: event.target.value })}
              >
                <option value="litigation">Litigation</option>
                <option value="transactional">Transactional</option>
                <option value="advisory">Advisory</option>
              </select>
            </label>
            <label>
              Jurisdiction
              <input
                value={caseForm.jurisdiction}
                onChange={(event) => setCaseForm({ ...caseForm, jurisdiction: event.target.value })}
              />
            </label>
            <label>
              Client ID
              <input
                value={caseForm.clientId}
                onChange={(event) => setCaseForm({ ...caseForm, clientId: event.target.value })}
              />
            </label>
            <button type="submit" disabled={loading}>
              {loading ? 'Saving…' : 'Create Case'}
            </button>
          </form>
        </div>
        <div>
          <h3>Active Matters</h3>
          <ul className="case-list">
            {cases.map((legalCase) => (
              <li
                key={legalCase.case_id || legalCase.caseId}
                className={selectedCaseId === legalCase.case_id ? 'selected' : ''}
                onClick={() => setSelectedCaseId(legalCase.case_id)}
              >
                <strong>{legalCase.case_title}</strong>
                <span className="muted">
                  {legalCase.case_type} · {legalCase.jurisdiction || 'Jurisdiction TBD'}
                </span>
              </li>
            ))}
            {!cases.length && <li>No cases created yet.</li>}
          </ul>
          <div className="analysis-controls">
            <label>
              Issues to analyse
              <input
                type="text"
                value={analysisIssues.join(', ')}
                onChange={(event) => setAnalysisIssues(event.target.value.split(',').map((item) => item.trim()))}
              />
            </label>
            <button type="button" onClick={handleAnalyseCase} disabled={!selectedCaseId || loading}>
              {loading ? 'Analyzing…' : 'Run Case Analysis'}
            </button>
          </div>
        </div>
      </div>

      {analysis && (
        <div className="analysis-panel">
          <h3>Case Analysis</h3>
          <p className="analysis-text">{analysis.analysis}</p>
          <h4>Similar Cases</h4>
          <ul>
            {analysis.similarCases?.map((item, index) => (
              <li key={`${item.case_name}-${index}`}>
                <strong>{item.case_name}</strong>
                <span className="muted">{item.jurisdiction}</span>
              </li>
            ))}
            {!analysis.similarCases?.length && <li>No similar cases returned by the agent.</li>}
          </ul>
        </div>
      )}
    </Card>
  );
};

CaseManagementPanel.propTypes = {
  attorneyId: PropTypes.string.isRequired,
  onCaseSelected: PropTypes.func,
};

export default CaseManagementPanel;
