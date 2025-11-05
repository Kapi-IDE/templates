import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Card from './Card';
import { analyzeLegalDocument } from '../services/api';

const DocumentAnalysisPanel = ({ attorneyId, clientId, caseId }) => {
  const [documentType, setDocumentType] = useState('contract');
  const [documentText, setDocumentText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (event) => {
    event.preventDefault();
    if (!documentText.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const analysis = await analyzeLegalDocument({
        attorneyId,
        clientId,
        caseId,
        documentType,
        documentText,
      });
      setResult(analysis);
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      title="Document Analysis"
      subtitle="Identify risk and obligations inside privileged documents"
    >
      <form className="stack" onSubmit={handleAnalyze}>
        <div className="grid cols-2">
          <label>
            Document Type
            <select value={documentType} onChange={(event) => setDocumentType(event.target.value)}>
              <option value="contract">Contract</option>
              <option value="brief">Brief</option>
              <option value="motion">Motion</option>
              <option value="discovery">Discovery</option>
            </select>
          </label>
          <label>
            Case ID (optional)
            <input
              type="text"
              value={caseId || ''}
              readOnly
              placeholder="Linked after case creation"
            />
          </label>
        </div>
        <label>
          Document Text
          <textarea
            rows="6"
            placeholder="Paste document text or clauses to review"
            value={documentText}
            onChange={(event) => setDocumentText(event.target.value)}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing…' : 'Analyze Document'}
        </button>
      </form>

      {error && <div className="alert alert--error">{error}</div>}
      {result && (
        <div className="grid cols-2 analysis-results">
          <div>
            <h3>AI Assessment</h3>
            <p className="analysis-text">{result.analysis}</p>
            <h4>Risks & Recommendations</h4>
            <ul>
              {result.risks?.map((risk, index) => (
                <li key={`${risk.description}-${index}`}>
                  <strong>{risk.severity.toUpperCase()}</strong>: {risk.description}
                  <p className="muted">Mitigation: {risk.mitigation}</p>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3>Related Templates</h3>
            <ul className="template-list">
              {result.relatedTemplates?.map((template, index) => (
                <li key={`${template.template_name}-${index}`}>
                  <strong>{template.template_name}</strong>
                  <p className="muted">{template.summary}</p>
                </li>
              ))}
              {!result.relatedTemplates?.length && <li>No related templates returned.</li>}
            </ul>
          </div>
        </div>
      )}
    </Card>
  );
};

DocumentAnalysisPanel.propTypes = {
  attorneyId: PropTypes.string.isRequired,
  clientId: PropTypes.string,
  caseId: PropTypes.string,
};

export default DocumentAnalysisPanel;
