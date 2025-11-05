/**
 * RAG Chat UI - React component with FastAPI backend integration
 *
 * Features:
 * - Authentication with JWT
 * - Document upload
 * - RAG-powered chat
 * - Source citations
 * - Streaming responses
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Loader2,
  Upload,
  LogOut,
  FileText,
  MessageCircle,
  ChevronDown,
} from 'lucide-react';

// Types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
}

interface Source {
  source: string;
  chunk_index: number;
  file_path: string;
}

interface UploadedFile {
  name: string;
  uploadedAt: Date;
}

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// API Client
class APIClient {
  private token: string | null = null;

  async login(email: string, password: string): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/login/access-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    const data = await response.json();
    this.token = data.access_token;
    return this.token;
  }

  async query(question: string, nResults: number = 3) {
    if (!this.token) throw new Error('Not authenticated');

    const response = await fetch(`${API_BASE_URL}/rag/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question, n_results: nResults }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Query failed');
    }

    return response.json();
  }

  async uploadFile(file: File) {
    if (!this.token) throw new Error('Not authenticated');

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/rag/upload`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${this.token}` },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    return response.json();
  }

  logout() {
    this.token = null;
  }

  getToken() {
    return this.token;
  }
}

const apiClient = new APIClient();

export default function RAGChatUI() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState('');

  // Chat state
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // File upload state
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // UI state
  const [showSources, setShowSources] = useState<{ [key: string]: boolean }>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Authentication handlers
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError('');

    try {
      await apiClient.login(email, password);
      setIsAuthenticated(true);
      setEmail('');
      setPassword('');
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : 'Login failed');
    }
  };

  const handleLogout = () => {
    apiClient.logout();
    setIsAuthenticated(false);
    setMessages([]);
    setUploadedFiles([]);
  };

  // Chat handlers
  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await apiClient.query(input);

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to get response'}`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // File upload handlers
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);

    try {
      await apiClient.uploadFile(file);

      setUploadedFiles(prev => [...prev, {
        name: file.name,
        uploadedAt: new Date(),
      }]);

      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  // Toggle source visibility
  const toggleSources = (messageId: string) => {
    setShowSources(prev => ({
      ...prev,
      [messageId]: !prev[messageId],
    }));
  };

  // Login screen
  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg w-96">
          <div className="flex items-center gap-3 mb-6">
            <MessageCircle size={32} className="text-blue-500" />
            <h1 className="text-2xl font-bold">RAG Assistant</h1>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="admin@example.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="••••••••"
                required
              />
            </div>

            {authError && (
              <div className="text-red-500 text-sm">{authError}</div>
            )}

            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors"
            >
              Login
            </button>
          </form>

          <p className="mt-4 text-sm text-gray-500 text-center">
            Use your FastAPI backend credentials
          </p>
        </div>
      </div>
    );
  }

  // Main chat interface
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 bg-gray-900 text-white p-4 flex flex-col">
        <div className="mb-6">
          <h1 className="text-xl font-bold mb-2">RAG Assistant</h1>
          <p className="text-sm text-gray-400">Ask questions about your documents</p>
        </div>

        {/* File Upload */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-400 mb-2">Upload Documents</h3>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.txt"
            onChange={handleFileUpload}
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-md transition-colors disabled:bg-gray-600"
          >
            {isUploading ? (
              <><Loader2 className="animate-spin" size={16} /> Uploading...</>
            ) : (
              <><Upload size={16} /> Upload File</>
            )}
          </button>
        </div>

        {/* Uploaded Files */}
        {uploadedFiles.length > 0 && (
          <div className="mb-6 flex-1 overflow-y-auto">
            <h3 className="text-sm font-semibold text-gray-400 mb-2">Uploaded Files</h3>
            <div className="space-y-2">
              {uploadedFiles.map((file, idx) => (
                <div key={idx} className="flex items-center gap-2 text-sm p-2 bg-gray-800 rounded">
                  <FileText size={14} />
                  <span className="truncate">{file.name}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 text-red-400 hover:text-red-300 transition-colors"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 mt-20">
                <MessageCircle size={48} className="mx-auto mb-4 text-gray-400" />
                <p className="text-lg">Start a conversation</p>
                <p className="text-sm">Upload documents and ask questions</p>
              </div>
            )}

            {messages.map((message) => (
              <div key={message.id} className="animate-in fade-in slide-in-from-bottom-2">
                <div
                  className={`rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-blue-50 border border-blue-200 ml-auto max-w-2xl'
                      : 'bg-white border border-gray-200 mr-auto max-w-3xl shadow-sm'
                  }`}
                >
                  <div className="text-xs text-gray-500 mb-1">
                    {message.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <p className="text-gray-800 whitespace-pre-wrap">{message.content}</p>

                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-3">
                      <button
                        onClick={() => toggleSources(message.id)}
                        className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800"
                      >
                        <ChevronDown
                          size={14}
                          className={`transition-transform ${
                            showSources[message.id] ? '' : '-rotate-90'
                          }`}
                        />
                        <span>Sources ({message.sources.length})</span>
                      </button>

                      {showSources[message.id] && (
                        <div className="mt-2 pl-4 space-y-1">
                          {message.sources.map((source, idx) => (
                            <div key={idx} className="text-xs text-gray-600">
                              • {source.source} (chunk {source.chunk_index})
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex items-center gap-3 text-gray-500 bg-white border border-gray-200 rounded-lg p-4 max-w-3xl shadow-sm">
                <Loader2 className="animate-spin" size={18} />
                <span>Thinking...</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-2">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about your documents..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={1}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !input.trim()}
                className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
