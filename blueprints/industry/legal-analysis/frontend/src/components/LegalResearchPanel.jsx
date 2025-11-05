import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Card from './Card';
import { runLegalResearch, searchPrecedents } from '../services/api';

const defaultFilters = {
  jurisdiction: '',
  limit: 10,
};

const LegalResearchPanel = ({ attorneyId, clientId }) => {
  const [question, setQuestion] = useState('');
  const [filters, setFilters] = useState(defaultFilters);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [researchResult, setResearchResult] = useState(null);
  const [precedentResult, setPrecedentResult] = useState(null);

  const handleResearch = async (event) => {
    event.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const packet = await runLegalResearch({
        question,
        attorneyId,
        clientId,
        jurisdiction: filters.jurisdiction || undefined,
        limit: Number(filters.limit) || 10,
      });
      setResearchResult(packet);

      const precedents = await searchPrecedents({
        legalIssue: question,
        attorneyId,
        clientId,
        jurisdiction: filters.jurisdiction || undefined,
      });
      setPrecedentResult(precedents);
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      title="Legal Research"
      subtitle="Run multi-source research with ethics guardrails"
      actions={
        <form className="inline-form" onSubmit={handleResearch}>
          <input
            type="text"
            placeholder="Enter research question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />
          <input
            type="text"
            placeholder="Jurisdiction (optional)"
            value={filters.jurisdiction}
            onChange={(event) => setFilters({ ...filters, jurisdiction: event.target.value })}
          />
          <input
            type="number"
            min="3"
            max="25"
            value={filters.limit}
            onChange={(event) => setFilters({ ...filters, limit: event.target.value })}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Researching…' : 'Run Research'}
          </button>
        </form>
      }
    >
      {error && <div className="alert alert--error">{error}</div>}
      {!researchResult && !loading && <p className="placeholder">Submit a question to see research results.</p>}

      {researchResult && (
        <div className="grid cols-2">
          <div>
            <h3>Research Memorandum</h3>
            <p className="analysis-text">{researchResult.analysis}</p>
            {researchResult.ethics && (
              <div className="tag">Ethics: {researchResult.ethics.compliance_status}</div>
            )}
          </div>
          <div>
            <h3>Key Authorities</h3>
            <ul className="authority-list">
              {researchResult.authorities?.map((authority, index) => (
                <li key={`${authority.citation || authority.title}-${index}`}>
                  <span className="authority-type">{authority.type}</span>
                  <div>
                    <strong>{authority.title}</strong>
                    {authority.citation && <span className="muted"> – {authority.citation}</span>}
                    <p>{authority.summary}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {precedentResult && (
        <div className="precedent-panel">
          <h3>Suggested Precedents</h3>
          <ul>
            {precedentResult.precedents?.map((precedent, index) => (
              <li key={`${precedent.legal_principle || 'precedent'}-${index}`}>
                <strong>{precedent.legal_principle || 'Precedent'}</strong>
                <span className="muted"> {precedent.citation}</span>
                <p>{precedent.summary}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
};

LegalResearchPanel.propTypes = {
  attorneyId: PropTypes.string.isRequired,
  clientId: PropTypes.string,
};

export default LegalResearchPanel;
