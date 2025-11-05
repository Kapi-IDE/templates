import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Card from './Card';
import { sendPrivilegedMessage, startPrivilegedSession } from '../services/api';

const PrivilegedChatPanel = ({ attorneyId, clientId }) => {
  const [session, setSession] = useState(null);
  const [message, setMessage] = useState('');
  const [transcript, setTranscript] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const ensureSession = async () => {
    if (session) {
      return session;
    }
    const newSession = await startPrivilegedSession({ attorneyId, clientId });
    setSession(newSession);
    return newSession;
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const activeSession = await ensureSession();
      const response = await sendPrivilegedMessage({
        sessionId: activeSession.session_id,
        sessionToken: activeSession.session_token,
        attorneyId,
        clientId,
        message,
      });

      setTranscript((entries) => [
        ...entries,
        { role: 'client', text: message },
        { role: 'ai', text: response.response },
      ]);
      setMessage('');
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      title="Privileged Chat"
      subtitle="Maintain attorney-client privilege with audit trails"
    >
      {error && <div className="alert alert--error">{error}</div>}
      <div className="chat-transcript">
        {transcript.length === 0 && <p className="placeholder">Start a conversation to see privileged responses.</p>}
        {transcript.map((entry, index) => (
          <div key={`${entry.role}-${index}`} className={`chat-bubble chat-bubble--${entry.role}`}>
            <span>{entry.text}</span>
          </div>
        ))}
      </div>
      <form className="chat-composer" onSubmit={handleSendMessage}>
        <textarea
          rows="2"
          placeholder="Ask a privileged question…"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending…' : 'Send Secure Message'}
        </button>
      </form>
      {session && (
        <p className="muted session-info">
          Session active · Expires {session.expires_at}
        </p>
      )}
    </Card>
  );
};

PrivilegedChatPanel.propTypes = {
  attorneyId: PropTypes.string.isRequired,
  clientId: PropTypes.string.isRequired,
};

export default PrivilegedChatPanel;
