const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json();
  if (!response.ok) {
    const error = new Error(data?.error || 'Request failed');
    error.status = response.status;
    throw error;
  }
  return data;
}

export function getHealth() {
  return request('/api/health');
}

export function runLegalResearch(payload) {
  return request('/api/research', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function analyzeLegalDocument(payload) {
  return request('/api/analyze-document', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function listCases(query = {}) {
  const params = new URLSearchParams(query).toString();
  return request(`/api/cases${params ? `?${params}` : ''}`);
}

export function createCase(payload) {
  return request('/api/cases', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateCase(caseId, payload) {
  return request(`/api/cases/${caseId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function analyzeCase(caseId, payload) {
  return request(`/api/cases/${caseId}/analysis`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function searchPrecedents(payload) {
  return request('/api/precedents/search', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function startPrivilegedSession(payload) {
  return request('/api/privileged-chat/session', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function sendPrivilegedMessage(payload) {
  return request('/api/privileged-chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getEthicsAudit(query = {}) {
  const params = new URLSearchParams(query).toString();
  return request(`/api/ethics/audit${params ? `?${params}` : ''}`);
}
