# React Chat UI Integration Examples

Complete examples for integrating the Onyx chat UI with various setups.

---

## Example 1: Next.js App Router

Full Next.js 14+ integration with server components.

### Setup

```bash
# Create Next.js app
npx create-next-app@latest my-chat-app --typescript --tailwind --app

# Copy component
cp -r templates/components/frontend/react-chat-ui my-chat-app/src/components/chat
```

### Implementation

```tsx
// app/page.tsx
import OnyxChatClone from '@/components/chat/OnyxChatClone';

export default function Home() {
  return (
    <main className="h-screen">
      <OnyxChatClone />
    </main>
  );
}
```

```tsx
// app/layout.tsx
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'RAG Chat Assistant',
  description: 'AI-powered chat with document Q&A',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
```

---

## Example 2: Vite + React

Standalone React app with Vite.

### Setup

```bash
# Create Vite app
npm create vite@latest my-chat-app -- --template react-ts

# Install dependencies
cd my-chat-app
npm install lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Copy component
cp -r templates/components/frontend/react-chat-ui src/components/chat
```

### Implementation

```tsx
// src/App.tsx
import OnyxChatClone from './components/chat/OnyxChatClone';

function App() {
  return (
    <div className="h-screen w-screen">
      <OnyxChatClone />
    </div>
  );
}

export default App;
```

```tsx
// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #root {
  height: 100%;
}
```

---

## Example 3: FastAPI Backend Integration

Connect to FastAPI RAG backend with authentication.

### API Client

```tsx
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface QueryResponse {
  answer: string;
  sources: Array<{
    source: string;
    chunk_index: number;
    file_path: string;
  }>;
  context_used: string[];
}

export class APIClient {
  private token: string | null = null;

  async login(email: string, password: string): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/login/access-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password }),
    });

    if (!response.ok) throw new Error('Login failed');

    const data: LoginResponse = await response.json();
    this.token = data.access_token;
    return this.token;
  }

  async query(question: string, nResults: number = 3): Promise<QueryResponse> {
    if (!this.token) throw new Error('Not authenticated');

    const response = await fetch(`${API_BASE_URL}/rag/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question, n_results: nResults }),
    });

    if (!response.ok) throw new Error('Query failed');
    return response.json();
  }

  async uploadFile(file: File): Promise<void> {
    if (!this.token) throw new Error('Not authenticated');

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/rag/upload`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${this.token}` },
      body: formData,
    });

    if (!response.ok) throw new Error('Upload failed');
  }

  logout() {
    this.token = null;
  }
}

export const apiClient = new APIClient();
```

### Modified Chat Component

```tsx
// components/RAGChatUI.tsx
import React, { useState } from 'react';
import { Send, Loader2, LogOut, Upload } from 'lucide-react';
import { apiClient } from '@/lib/api';

export default function RAGChatUI() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [messages, setMessages] = useState<Array<{
    role: 'user' | 'assistant';
    content: string;
    sources?: any[];
  }>>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    try {
      await apiClient.login(email, password);
      setIsAuthenticated(true);
    } catch (error) {
      alert('Login failed');
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await apiClient.query(input);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request.',
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    try {
      await apiClient.uploadFile(file);
      alert('File uploaded successfully!');
    } catch (error) {
      alert('Upload failed');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg w-96">
          <h2 className="text-2xl font-bold mb-4">Login</h2>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded mb-3"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded mb-4"
          />
          <button
            onClick={handleLogin}
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-80 bg-gray-900 text-white p-4">
        <h1 className="text-xl font-bold mb-4">RAG Assistant</h1>

        <label className="block mb-2">
          <span className="text-sm">Upload Document</span>
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFileUpload(file);
            }}
            className="block w-full text-sm mt-1"
          />
        </label>

        <button
          onClick={() => {
            apiClient.logout();
            setIsAuthenticated(false);
            setMessages([]);
          }}
          className="mt-4 flex items-center gap-2 text-red-400 hover:text-red-300"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>

      {/* Main Chat */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`mb-4 p-3 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-100 ml-auto max-w-md'
                  : 'bg-gray-200 mr-auto max-w-2xl'
              }`}
            >
              <p>{msg.content}</p>
              {msg.sources && (
                <details className="mt-2 text-sm text-gray-600">
                  <summary>Sources</summary>
                  {msg.sources.map((s, i) => (
                    <div key={i}>• {s.source}</div>
                  ))}
                </details>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center gap-2 text-gray-500">
              <Loader2 className="animate-spin" size={16} />
              Thinking...
            </div>
          )}
        </div>

        <div className="p-4 border-t">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder="Ask about your documents..."
              className="flex-1 p-2 border rounded"
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !input.trim()}
              className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## Example 4: Streaming Responses

Real-time streaming from FastAPI backend.

```tsx
// lib/streaming.ts
export async function* streamQuery(
  question: string,
  token: string
): AsyncGenerator<string> {
  const response = await fetch(`${API_BASE_URL}/rag/query/stream`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question, n_results: 3 }),
  });

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) throw new Error('No reader');

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: true });
    yield chunk;
  }
}
```

```tsx
// Use in component
const handleStreamMessage = async () => {
  setMessages(prev => [...prev, { role: 'user', content: input }]);

  let assistantMessage = '';
  setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

  for await (const chunk of streamQuery(input, token)) {
    assistantMessage += chunk;
    setMessages(prev => {
      const newMessages = [...prev];
      newMessages[newMessages.length - 1].content = assistantMessage;
      return newMessages;
    });
  }
};
```

---

## Example 5: Environment Configuration

Manage API URLs across environments.

```bash
# .env.local (development)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# .env.production
NEXT_PUBLIC_API_URL=https://api.yourapp.com/api/v1
```

```tsx
// config/api.ts
export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  isDevelopment: process.env.NODE_ENV === 'development',
};
```

---

## Example 6: Error Handling

Comprehensive error handling.

```tsx
// lib/errors.ts
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export async function fetchWithError(url: string, options?: RequestInit) {
  const response = await fetch(url, options);

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new APIError(
      data?.detail || 'Request failed',
      response.status,
      data
    );
  }

  return response.json();
}
```

```tsx
// Use in component
try {
  const result = await fetchWithError(`${API_URL}/rag/query`, {
    method: 'POST',
    headers: { /* ... */ },
    body: JSON.stringify(/* ... */),
  });
} catch (error) {
  if (error instanceof APIError) {
    if (error.status === 401) {
      // Handle unauthorized
      router.push('/login');
    } else {
      alert(error.message);
    }
  }
}
```

---

## Example 7: TypeScript Types

Shared types for type safety.

```tsx
// types/chat.ts
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: Source[];
}

export interface Source {
  source: string;
  chunk_index: number;
  file_path: string;
}

export interface Assistant {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}
```

---

## Production Best Practices

### 1. Authentication State Management

```tsx
// hooks/useAuth.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  user: { email: string } | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      login: async (email, password) => {
        const token = await apiClient.login(email, password);
        set({ token, user: { email } });
      },
      logout: () => {
        apiClient.logout();
        set({ token: null, user: null });
      },
    }),
    { name: 'auth-storage' }
  )
);
```

### 2. Message Persistence

```tsx
// hooks/useMessages.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useMessages = create(
  persist(
    (set) => ({
      messages: [],
      addMessage: (message) =>
        set((state) => ({ messages: [...state.messages, message] })),
      clearMessages: () => set({ messages: [] }),
    }),
    { name: 'chat-messages' }
  )
);
```

### 3. API Rate Limiting

```tsx
// lib/rate-limiter.ts
export class RateLimiter {
  private requests: number[] = [];
  private limit: number;
  private window: number;

  constructor(limit: number = 10, windowMs: number = 60000) {
    this.limit = limit;
    this.window = windowMs;
  }

  async checkLimit(): Promise<boolean> {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.window);

    if (this.requests.length >= this.limit) {
      return false;
    }

    this.requests.push(now);
    return true;
  }
}

const rateLimiter = new RateLimiter(10, 60000);

// Use before API calls
if (!await rateLimiter.checkLimit()) {
  throw new Error('Rate limit exceeded');
}
```

---

## Deployment

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

### Docker

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api/v1
    depends_on:
      - backend

  backend:
    image: fastapi-rag-starter
    ports:
      - "8000:8000"
```

---

For more examples, see the component README and FastAPI backend documentation.
