import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import TriageDisplay from './components/TriageDisplay';
import HealthCheck from './components/HealthCheck';
import PatientIntakeForm from './components/PatientIntakeForm';
import './App.css';

function App() {
  const [patientId, setPatientId] = useState(null);
  const [sessionActive, setSessionActive] = useState(false);
  const [triageData, setTriageData] = useState(null);
  const [systemHealth, setSystemHealth] = useState(null);
  const [showIntakeForm, setShowIntakeForm] = useState(false);
  const [patientInfo, setPatientInfo] = useState(null);

  useEffect(() => {
    // Check system health on startup
    checkSystemHealth();
  }, []);

  const checkSystemHealth = async () => {
    try {
      const response = await fetch('http://localhost:8083/api/health');
      const data = await response.json();
      setSystemHealth(data);
    } catch (error) {
      console.error('Health check failed:', error);
      setSystemHealth({ status: 'unhealthy', error: error.message });
    }
  };

  const startPatientSession = async () => {
    const newPatientId = `patient_${Date.now()}`;
    
    try {
      const response = await fetch('http://localhost:8083/api/patient/start-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ patient_id: newPatientId }),
      });

      if (response.ok) {
        setPatientId(newPatientId);
        setShowIntakeForm(true); // Show intake form first
        setTriageData(null); // Reset triage data for new session
      } else {
        console.error('Failed to start session');
      }
    } catch (error) {
      console.error('Session start error:', error);
    }
  };

  const handleTriageUpdate = (newTriageData) => {
    setTriageData(newTriageData);
  };

  const handleIntakeSubmit = (formData) => {
    setPatientInfo(formData);
    setShowIntakeForm(false);
    setSessionActive(true);
  };

  const handleIntakeSkip = () => {
    setShowIntakeForm(false);
    setSessionActive(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 shadow-lg">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold flex items-center">
            🏥 Healthcare AI Pod
          </h1>
          <div className="flex items-center space-x-4">
            <HealthCheck health={systemHealth} />
            {sessionActive && (
              <div className="flex items-center space-x-3">
                <span className="text-sm bg-blue-700 px-3 py-1 rounded-full">
                  Session: {patientId}
                </span>
                {patientInfo && (
                  <span className="text-sm bg-green-600 px-3 py-1 rounded-full">
                    📄 Intake Complete
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="container mx-auto p-4">
        {showIntakeForm ? (
          <PatientIntakeForm 
            onSubmit={handleIntakeSubmit}
            onSkip={handleIntakeSkip}
          />
        ) : !sessionActive ? (
          <div className="max-w-md mx-auto mt-16 text-center">
            <div className="bg-white rounded-xl shadow-xl p-8 border border-blue-100">
              <div className="text-6xl mb-4">🩺</div>
              <h2 className="text-2xl font-bold text-blue-800 mb-4">AI-Powered Patient Triage</h2>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Our intelligent healthcare assistant will analyze your symptoms using advanced AI 
                to provide immediate triage assessment and medical guidance.
              </p>
              <div className="bg-blue-50 p-4 rounded-lg mb-6">
                <h3 className="font-semibold text-blue-800 mb-2">🤖 AI Capabilities:</h3>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Symptom analysis and urgency scoring</li>
                  <li>• Medical knowledge retrieval</li>
                  <li>• Escalation protocols</li>
                  <li>• Treatment recommendations</li>
                </ul>
              </div>
              <button
                onClick={startPatientSession}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-6 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                disabled={systemHealth?.status !== 'healthy'}
              >
                Start Patient Session
              </button>
              {systemHealth?.status !== 'healthy' && (
                <p className="text-red-500 text-sm mt-2">
                  System not ready. Please check system health.
                </p>
              )}
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Chat Interface - Main Column */}
            <div className="lg:col-span-2">
              <ChatInterface 
                patientId={patientId}
                onTriageUpdate={handleTriageUpdate}
              />
            </div>

            {/* Triage Display - Side Column */}
            <div className="lg:col-span-1">
              <TriageDisplay 
                triageData={triageData}
                patientId={patientId}
              />
            </div>
          </div>
        )}
      </main>

      <footer className="bg-gray-800 text-white p-4 mt-8">
        <div className="container mx-auto text-center text-sm">
          <p>Healthcare AI Pod - Modern AI Pro Practitioner Course</p>
          <p className="text-gray-400">Built with React + Flask + ChromaDB + Gemini AI</p>
        </div>
      </footer>
    </div>
  );
}

export default App;