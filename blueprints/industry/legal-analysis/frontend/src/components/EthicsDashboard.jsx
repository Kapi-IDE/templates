import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import Card from './Card';
import { getEthicsAudit } from '../services/api';

const EthicsDashboard = ({ attorneyId }) => {
  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAudit = async () => {
      setLoading(true);
      setError(null);
      try {
        const summary = await getEthicsAudit({ attorneyId });
        setAudit(summary);
      } catch (apiError) {
        setError(apiError.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAudit();
  }, [attorneyId]);

  return (
    <Card title="Ethics & Compliance" subtitle="Monitor privilege, disclosure, and technology competence">
      {loading && <p>Loading audit summary…</p>}
      {error && <div className="alert alert--error">{error}</div>}
      {audit && (
        <div className="ethics-grid">
          <div className="metric">
            <h4>Compliance Score</h4>
            <span className="metric__value">{audit.compliance_score || audit.overall_compliance || 0}%</span>
            <p className="muted">Rolling {audit.periodDays || 30}-day window</p>
          </div>
          <div className="metric">
            <h4>Privilege Events</h4>
            <span className="metric__value">{audit.privilege_events || 0}</span>
            <p className="muted">Logged communications</p>
          </div>
          <div className="metric">
            <h4>Disclosures Pending</h4>
            <span className="metric__value">{audit.pending_disclosures || 0}</span>
            <p className="muted">Clients awaiting AI disclosure</p>
          </div>
        </div>
      )}
      {!loading && !audit && !error && <p className="placeholder">No compliance data returned yet.</p>}
    </Card>
  );
};

EthicsDashboard.propTypes = {
  attorneyId: PropTypes.string.isRequired,
};

export default EthicsDashboard;
