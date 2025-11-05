'use client';

import { useState } from 'react';
import { LLMSelector } from '@/components/LLMSelector';
import type { LLMConfig } from '@/lib/universal-llm';

interface Message {
  role: 'user' | 'assistant' | 'thinking';
  content: string;
  steps?: AgentStep[];
  recommendation?: 'BUY' | 'SELL' | 'HOLD';
}

interface AgentStep {
  step: number;
  thought: string;
  action?: string;
  actionInput?: string;
  observation?: string;
}

export default function StockAgentPage() {
  const [llmConfig, setLlmConfig] = useState<LLMConfig | null>(null);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hi! I\'m your AI stock trading agent. Ask me about any stock!\n\nExample questions:\n• "Should I buy Tesla?"\n• "Compare Apple and Microsoft"\n• "Is NVIDIA a good investment?"'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(true);

  const sendMessage = async () => {
    if (!llmConfig || !input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Add thinking indicator
    const thinkingMessage: Message = {
      role: 'thinking',
      content: 'Analyzing...'
    };
    setMessages(prev => [...prev, thinkingMessage]);

    try {
      const response = await fetch('/api/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: input,
          llmConfig
        })
      });

      const data = await response.json();

      // Remove thinking indicator
      setMessages(prev => prev.filter(m => m.role !== 'thinking'));

      if (data.success) {
        // Extract recommendation from answer
        let recommendation: 'BUY' | 'SELL' | 'HOLD' | undefined;
        if (data.answer.includes('BUY')) recommendation = 'BUY';
        else if (data.answer.includes('SELL')) recommendation = 'SELL';
        else if (data.answer.includes('HOLD')) recommendation = 'HOLD';

        const assistantMessage: Message = {
          role: 'assistant',
          content: data.answer,
          steps: data.steps,
          recommendation
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `Error: ${data.error}`
        }]);
      }

    } catch (error) {
      setMessages(prev => prev.filter(m => m.role !== 'thinking'));
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            🤖 ReAct Stock Trading Agent
          </h1>
          <p className="text-slate-300">
            AI-powered stock analysis using the ReAct framework
          </p>
          <div className="mt-2 text-sm text-slate-400">
            ⚠️ Educational tool only - Not financial advice
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Settings Sidebar */}
          <div className={`lg:col-span-1 ${showSettings ? '' : 'hidden lg:block'}`}>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-white">⚙️ Settings</h2>
                <button
                  onClick={() => setShowSettings(false)}
                  className="lg:hidden text-white"
                >
                  ✕
                </button>
              </div>

              {/* LLM Selector Component */}
              <LLMSelector
                onConfigChange={setLlmConfig}
                showPricing={true}
                showModelSelection={true}
                showAdvancedSettings={true}
                className="bg-slate-800/50 border-slate-700"
              />

              {/* Current Config Display */}
              {llmConfig && (
                <div className="mt-6 p-4 bg-green-500/20 border border-green-500/50 rounded-lg">
                  <div className="text-green-300 text-sm font-semibold mb-2">
                    ✅ Agent Ready
                  </div>
                  <div className="text-white text-xs space-y-1">
                    <div>Provider: <span className="font-mono">{llmConfig.provider}</span></div>
                    <div>Model: <span className="font-mono">{llmConfig.model}</span></div>
                  </div>
                </div>
              )}

              {/* Info */}
              <div className="mt-6 p-4 bg-blue-500/20 border border-blue-500/50 rounded-lg">
                <div className="text-blue-300 text-sm font-semibold mb-2">
                  💡 How it works
                </div>
                <div className="text-white text-xs space-y-2">
                  <div>1. <strong>Think</strong> - Agent reasons</div>
                  <div>2. <strong>Act</strong> - Calls tools</div>
                  <div>3. <strong>Observe</strong> - Gets data</div>
                  <div>4. <strong>Repeat</strong> - Until answer</div>
                </div>
              </div>
            </div>
          </div>

          {/* Chat Area */}
          <div className="lg:col-span-2">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl border border-white/20 flex flex-col h-[calc(100vh-250px)]">
              {/* Chat Header */}
              <div className="p-4 border-b border-white/20 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-white font-semibold">Stock Analysis Chat</span>
                </div>
                <button
                  onClick={() => setShowSettings(true)}
                  className="lg:hidden px-3 py-1 bg-white/10 text-white rounded-lg text-sm"
                >
                  Settings
                </button>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-xl p-4 ${
                        msg.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : msg.role === 'thinking'
                          ? 'bg-yellow-500/20 border border-yellow-500/50 text-yellow-200'
                          : 'bg-white/10 text-white border border-white/20'
                      }`}
                    >
                      {/* User/Assistant Message */}
                      {msg.role !== 'thinking' && (
                        <div className="whitespace-pre-wrap">{msg.content}</div>
                      )}

                      {/* Thinking Indicator */}
                      {msg.role === 'thinking' && (
                        <div className="flex items-center gap-2">
                          <div className="flex gap-1">
                            <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce delay-100"></div>
                            <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce delay-200"></div>
                          </div>
                          <span>{msg.content}</span>
                        </div>
                      )}

                      {/* Recommendation Badge */}
                      {msg.recommendation && (
                        <div className="mt-3 pt-3 border-t border-white/20">
                          <div
                            className={`inline-block px-4 py-2 rounded-lg font-bold text-lg ${
                              msg.recommendation === 'BUY'
                                ? 'bg-green-500 text-white'
                                : msg.recommendation === 'SELL'
                                ? 'bg-red-500 text-white'
                                : 'bg-yellow-500 text-black'
                            }`}
                          >
                            {msg.recommendation === 'BUY' && '✅ BUY'}
                            {msg.recommendation === 'SELL' && '❌ SELL'}
                            {msg.recommendation === 'HOLD' && '⏸️ HOLD'}
                          </div>
                        </div>
                      )}

                      {/* Agent Steps (collapsible) */}
                      {msg.steps && msg.steps.length > 0 && (
                        <details className="mt-3 pt-3 border-t border-white/20">
                          <summary className="cursor-pointer text-sm text-slate-300 hover:text-white">
                            🧠 View Agent Thinking ({msg.steps.length} steps)
                          </summary>
                          <div className="mt-2 space-y-2 text-xs">
                            {msg.steps.map((step, i) => (
                              <div key={i} className="bg-black/20 p-2 rounded">
                                <div className="font-semibold text-blue-300">
                                  Step {step.step}
                                </div>
                                <div className="text-slate-300">
                                  💭 {step.thought}
                                </div>
                                {step.action && (
                                  <div className="text-green-300">
                                    ⚡ {step.action}: {step.actionInput}
                                  </div>
                                )}
                                {step.observation && (
                                  <div className="text-yellow-300">
                                    👁️ {step.observation.substring(0, 100)}
                                    {step.observation.length > 100 && '...'}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </details>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Input */}
              <div className="p-4 border-t border-white/20">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                    placeholder={
                      llmConfig
                        ? "Ask about any stock..."
                        : "Configure LLM provider first..."
                    }
                    disabled={!llmConfig || isLoading}
                    className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                  />
                  <button
                    onClick={sendMessage}
                    disabled={!llmConfig || !input.trim() || isLoading}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {isLoading ? '...' : 'Ask'}
                  </button>
                </div>

                {/* Example Questions */}
                {!isLoading && messages.length === 1 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {['Should I buy Tesla?', 'Compare AAPL and MSFT', 'Is NVIDIA a good buy?'].map((q) => (
                      <button
                        key={q}
                        onClick={() => setInput(q)}
                        disabled={!llmConfig}
                        className="px-3 py-1 bg-white/5 hover:bg-white/10 text-white text-sm rounded-lg border border-white/20 disabled:opacity-50"
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
