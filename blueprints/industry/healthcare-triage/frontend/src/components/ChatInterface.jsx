import React, { useState, useRef, useEffect } from 'react';

const ChatInterface = ({ patientId, onTriageUpdate }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message when patient ID changes
    if (patientId) {
      setMessages([{
        type: 'ai',
        content: '👋 Hello! I\'m your AI health assistant powered by advanced medical knowledge. Please describe your symptoms, and I\'ll provide immediate triage assessment with urgency scoring and medical guidance. How can I help you today?',
        timestamp: new Date().toISOString()
      }]);
    }
  }, [patientId]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8083/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.content,
          context: {}
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response
      const aiMessage = {
        type: 'ai',
        content: data.agent_response || 'I received your message and am processing it.',
        timestamp: data.timestamp || new Date().toISOString(),
        urgency: data.urgency_assessment,
        knowledge: data.medical_knowledge,
        escalation: data.escalation
      };

      setMessages(prev => [...prev, aiMessage]);

      // Update triage data if available
      if (data.urgency_assessment && onTriageUpdate) {
        onTriageUpdate({
          urgency_score: data.urgency_assessment.score,
          urgency_level: data.urgency_assessment.level,
          reasoning: data.urgency_assessment.reasoning,
          recommended_action: data.urgency_assessment.recommended_action,
          escalation: data.escalation,
          timestamp: data.timestamp
        });
      }

    } catch (error) {
      console.error('Message send error:', error);
      setError('Failed to send message. Please try again.');
      
      // Add error message
      const errorMessage = {
        type: 'error',
        content: 'Sorry, I\'m having technical difficulties. Please try again or contact a healthcare provider directly if this is urgent.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const MessageComponent = ({ message }) => {
    const isUser = message.type === 'user';
    const isError = message.type === 'error';

    return (
      <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
        <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
          isUser 
            ? 'bg-blue-600 text-white' 
            : isError 
              ? 'bg-red-100 text-red-800 border border-red-300'
              : 'bg-white text-gray-800 border border-gray-300'
        }`}>
          <div className="text-sm">{message.content}</div>
          <div className={`text-xs mt-1 ${
            isUser ? 'text-blue-200' : 'text-gray-500'
          }`}>
            {formatTimestamp(message.timestamp)}
          </div>
          
          {/* Show urgency info for AI messages */}
          {message.urgency && (
            <div className="mt-2 p-2 bg-gray-50 rounded text-xs">
              <div className="font-semibold">
                Urgency: {message.urgency.level} ({message.urgency.score}/10)
              </div>
              {message.urgency.reasoning && (
                <div className="mt-1">{message.urgency.reasoning}</div>
              )}
            </div>
          )}

          {/* Show escalation warning */}
          {message.escalation?.required && (
            <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs">
              <div className="font-semibold text-yellow-800">⚠️ Escalation Required</div>
              <div className="text-yellow-700">
                Level: {message.escalation.level}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-xl h-[600px] flex flex-col border border-blue-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 rounded-t-xl text-white">
        <h3 className="font-bold text-lg flex items-center">
          🤖 AI Health Assistant
        </h3>
        <p className="text-blue-100 text-sm mt-1">Describe your symptoms for intelligent medical triage</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <MessageComponent key={index} message={message} />
        ))}
        
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <div className="flex items-center space-x-2">
                <div className="animate-pulse flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                </div>
                <span className="text-sm text-gray-600">AI is analyzing...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        {error && (
          <div className="mb-2 p-2 bg-red-100 border border-red-300 rounded text-sm text-red-700">
            {error}
          </div>
        )}
        
        <div className="flex space-x-2">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="e.g., 'I have chest pain and shortness of breath' or 'Experiencing headache and fever for 2 days'"
            className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="2"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            Send
          </button>
        </div>
        
        <p className="text-xs text-gray-500 mt-2">
          Press Enter to send • This is for demonstration purposes only
        </p>
      </div>
    </div>
  );
};

export default ChatInterface;