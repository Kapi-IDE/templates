/**
 * Complete Chat App Example
 *
 * Demonstrates:
 * - LLMSelector component for provider selection
 * - Universal LLM Client for backend
 * - Streaming responses
 * - Cost tracking
 * - Multi-provider support
 */

'use client';

import { useState, useEffect } from 'react';
import { LLMSelector } from '@/components/LLMSelector';
import { createLLMClient, calculateCost } from '@/lib/universal-llm';
import type { LLMConfig, Message, ChatResponse } from '@/lib/universal-llm';

export default function ChatApp() {
  // State
  const [config, setConfig] = useState<LLMConfig | null>(null);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: 'You are a helpful assistant. Be concise and friendly.'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [totalCost, setTotalCost] = useState(0);
  const [showSettings, setShowSettings] = useState(true);

  // Auto-hide settings after config is set
  useEffect(() => {
    if (config) {
      setShowSettings(false);
    }
  }, [config]);

  // Send message
  const sendMessage = async () => {
    if (!config || !input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      // Create LLM client
      const client = createLLMClient(config);

      // Get response
      const response: ChatResponse = await client.chat({
        messages: newMessages,
        temperature: config.temperature,
        maxTokens: config.maxTokens
      });

      // Add assistant message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.content
      }]);

      // Track cost
      const cost = calculateCost(response);
      setTotalCost(prev => prev + cost);

    } catch (error) {
      console.error('Chat error:', error);
      alert(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Stream message (alternative to sendMessage)
  const sendMessageStreaming = async () => {
    if (!config || !input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const client = createLLMClient(config);

      // Add empty assistant message
      const assistantIndex = newMessages.length;
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      // Stream response
      for await (const chunk of client.chatStream({
        messages: newMessages,
        temperature: config.temperature,
        maxTokens: config.maxTokens
      })) {
        // Update assistant message with streaming content
        setMessages(prev => {
          const updated = [...prev];
          updated[assistantIndex] = {
            role: 'assistant',
            content: updated[assistantIndex].content + chunk.content
          };
          return updated;
        });

        if (chunk.done) break;
      }

    } catch (error) {
      console.error('Streaming error:', error);
      alert(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Clear chat
  const clearChat = () => {
    setMessages([{
      role: 'system',
      content: 'You are a helpful assistant. Be concise and friendly.'
    }]);
    setTotalCost(0);
  };

  return (
    <div className="chat-app">
      {/* Header */}
      <header className="header">
        <h1>Multi-LLM Chat</h1>
        <div className="header-actions">
          <button onClick={() => setShowSettings(!showSettings)}>
            {showSettings ? '💬 Chat' : '⚙️ Settings'}
          </button>
          <button onClick={clearChat}>🗑️ Clear</button>
          <div className="cost">
            Total Cost: ${totalCost.toFixed(6)}
          </div>
        </div>
      </header>

      <div className="main">
        {/* Sidebar - LLM Settings */}
        {showSettings && (
          <aside className="sidebar">
            <h2>LLM Configuration</h2>
            <LLMSelector
              onConfigChange={setConfig}
              showPricing={true}
              showModelSelection={true}
              showAdvancedSettings={true}
            />

            {config && (
              <div className="config-summary">
                <h3>Current Config</h3>
                <p><strong>Provider:</strong> {config.provider}</p>
                <p><strong>Model:</strong> {config.model}</p>
                <p><strong>Temperature:</strong> {config.temperature}</p>
                <p><strong>Max Tokens:</strong> {config.maxTokens}</p>
              </div>
            )}
          </aside>
        )}

        {/* Chat Area */}
        <main className="chat">
          {/* Messages */}
          <div className="messages">
            {messages
              .filter(m => m.role !== 'system')
              .map((msg, i) => (
                <div key={i} className={`message ${msg.role}`}>
                  <div className="message-header">
                    <strong>{msg.role === 'user' ? '👤 You' : '🤖 Assistant'}</strong>
                  </div>
                  <div className="message-content">
                    {msg.content}
                  </div>
                </div>
              ))}

            {isLoading && (
              <div className="message assistant loading">
                <div className="message-header">
                  <strong>🤖 Assistant</strong>
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              placeholder={config ? "Type a message..." : "Configure LLM first..."}
              disabled={!config || isLoading}
              className="input"
            />
            <button
              onClick={sendMessage}
              disabled={!config || !input.trim() || isLoading}
              className="send-button"
            >
              Send
            </button>
            <button
              onClick={sendMessageStreaming}
              disabled={!config || !input.trim() || isLoading}
              className="stream-button"
              title="Send with streaming"
            >
              Stream
            </button>
          </div>
        </main>
      </div>

      <style jsx>{`
        .chat-app {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background: #f9fafb;
        }

        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 1rem 1.5rem;
          background: white;
          border-bottom: 1px solid #e5e7eb;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
          margin: 0;
          font-size: 1.5rem;
          color: #111827;
        }

        .header-actions {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .header-actions button {
          padding: 0.5rem 1rem;
          border: 1px solid #d1d5db;
          border-radius: 0.375rem;
          background: white;
          cursor: pointer;
          font-size: 0.875rem;
        }

        .header-actions button:hover {
          background: #f3f4f6;
        }

        .cost {
          padding: 0.5rem 1rem;
          background: #ecfdf5;
          border: 1px solid #a7f3d0;
          border-radius: 0.375rem;
          font-size: 0.875rem;
          font-weight: 600;
          color: #065f46;
        }

        .main {
          display: flex;
          flex: 1;
          overflow: hidden;
        }

        .sidebar {
          width: 350px;
          padding: 1.5rem;
          background: white;
          border-right: 1px solid #e5e7eb;
          overflow-y: auto;
        }

        .sidebar h2 {
          margin-top: 0;
          font-size: 1.25rem;
          color: #111827;
        }

        .config-summary {
          margin-top: 1.5rem;
          padding: 1rem;
          background: #f3f4f6;
          border-radius: 0.5rem;
        }

        .config-summary h3 {
          margin-top: 0;
          font-size: 1rem;
          color: #111827;
        }

        .config-summary p {
          margin: 0.5rem 0;
          font-size: 0.875rem;
          color: #4b5563;
        }

        .chat {
          display: flex;
          flex-direction: column;
          flex: 1;
          background: white;
        }

        .messages {
          flex: 1;
          padding: 1.5rem;
          overflow-y: auto;
        }

        .message {
          margin-bottom: 1.5rem;
          max-width: 70%;
        }

        .message.user {
          margin-left: auto;
        }

        .message.assistant {
          margin-right: auto;
        }

        .message-header {
          margin-bottom: 0.5rem;
          font-size: 0.875rem;
          color: #6b7280;
        }

        .message-content {
          padding: 1rem;
          border-radius: 0.75rem;
          line-height: 1.6;
        }

        .message.user .message-content {
          background: #3b82f6;
          color: white;
        }

        .message.assistant .message-content {
          background: #f3f4f6;
          color: #111827;
        }

        .typing-indicator {
          display: flex;
          gap: 0.25rem;
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          background: #9ca3af;
          border-radius: 50%;
          animation: typing 1.4s infinite;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes typing {
          0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
          }
          30% {
            transform: translateY(-10px);
            opacity: 1;
          }
        }

        .input-area {
          display: flex;
          gap: 0.75rem;
          padding: 1.5rem;
          border-top: 1px solid #e5e7eb;
          background: white;
        }

        .input {
          flex: 1;
          padding: 0.75rem 1rem;
          border: 1px solid #d1d5db;
          border-radius: 0.5rem;
          font-size: 0.9375rem;
        }

        .input:focus {
          outline: 2px solid #3b82f6;
          outline-offset: 2px;
          border-color: #3b82f6;
        }

        .send-button,
        .stream-button {
          padding: 0.75rem 1.5rem;
          border: none;
          border-radius: 0.5rem;
          background: #3b82f6;
          color: white;
          font-weight: 600;
          cursor: pointer;
        }

        .stream-button {
          background: #8b5cf6;
        }

        .send-button:hover {
          background: #2563eb;
        }

        .stream-button:hover {
          background: #7c3aed;
        }

        .send-button:disabled,
        .stream-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
}
