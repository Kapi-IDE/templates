# LLM Selector Component

**Reusable React Component** - UI for selecting and configuring LLM providers

## ✨ Features

- **5 LLM Providers**: OpenAI, Azure OpenAI, Gemini, Claude, Ollama
- **Interactive UI**: Dropdown selection with provider-specific configuration
- **Built-in Pricing**: Shows cost information for each provider
- **Model Selection**: Choose from available models per provider
- **Advanced Settings**: Temperature, max tokens, etc.
- **Compact Mode**: Smaller UI for space-constrained layouts
- **Type-Safe**: Full TypeScript support
- **Styled**: Default styles included, fully customizable

## 🚀 Quick Start

### Installation

```bash
# Copy component to your project
cp LLMSelector.tsx your-project/components/
```

### Basic Usage

```tsx
'use client';

import { useState } from 'react';
import { LLMSelector } from '@/components/LLMSelector';
import type { LLMConfig } from '@/lib/universal-llm';

export default function MyApp() {
  const [config, setConfig] = useState<LLMConfig | null>(null);

  return (
    <div>
      <h1>Choose Your LLM</h1>

      <LLMSelector
        onConfigChange={setConfig}
        showPricing={true}
        showModelSelection={true}
      />

      {config && (
        <p>Selected: {config.provider} - {config.model}</p>
      )}
    </div>
  );
}
```

## 📖 Props

```typescript
interface LLMSelectorProps {
  /** Callback when configuration changes */
  onConfigChange?: (config: LLMConfig | null) => void;

  /** Initial provider selection */
  defaultProvider?: LLMProvider;

  /** Initial configuration */
  defaultConfig?: Partial<LLMConfig>;

  /** Show pricing information */
  showPricing?: boolean;

  /** Show model selection dropdown */
  showModelSelection?: boolean;

  /** Show advanced settings (temperature, maxTokens, etc.) */
  showAdvancedSettings?: boolean;

  /** Allowed providers (default: all) */
  allowedProviders?: LLMProvider[];

  /** Custom styling */
  className?: string;

  /** Compact mode (smaller UI) */
  compact?: boolean;
}
```

## 🎯 Usage Examples

### With Chat Interface

```tsx
'use client';

import { useState } from 'react';
import { LLMSelector } from '@/components/LLMSelector';
import { createLLMClient } from '@/lib/universal-llm';
import type { LLMConfig, Message } from '@/lib/universal-llm';

export default function ChatApp() {
  const [config, setConfig] = useState<LLMConfig | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!config || !input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    // Call LLM
    const client = createLLMClient(config);
    const response = await client.chat({
      messages: [...messages, userMessage]
    });

    setMessages(prev => [...prev, {
      role: 'assistant',
      content: response.content
    }]);
  };

  return (
    <div className="chat-app">
      {/* LLM Configuration */}
      <div className="sidebar">
        <h2>LLM Settings</h2>
        <LLMSelector
          onConfigChange={setConfig}
          showPricing={true}
          showModelSelection={true}
          showAdvancedSettings={true}
        />
      </div>

      {/* Chat Interface */}
      <div className="chat">
        <div className="messages">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <strong>{msg.role}:</strong> {msg.content}
            </div>
          ))}
        </div>

        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type a message..."
            disabled={!config}
          />
          <button onClick={sendMessage} disabled={!config}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
```

### Compact Mode (Settings Page)

```tsx
<LLMSelector
  compact={true}
  defaultProvider="gemini"
  showPricing={false}
  onConfigChange={setConfig}
/>
```

### Limited Providers

```tsx
// Only show free or cheap options
<LLMSelector
  allowedProviders={['ollama', 'gemini', 'openai']}
  defaultProvider="ollama"
  onConfigChange={setConfig}
/>
```

### With Persistence

```tsx
'use client';

import { useState, useEffect } from 'react';
import { LLMSelector } from '@/components/LLMSelector';
import type { LLMConfig } from '@/lib/universal-llm';

export default function PersistentSettings() {
  const [config, setConfig] = useState<LLMConfig | null>(null);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('llm-config');
    if (saved) {
      setConfig(JSON.parse(saved));
    }
  }, []);

  // Save to localStorage when config changes
  useEffect(() => {
    if (config) {
      localStorage.setItem('llm-config', JSON.stringify(config));
    }
  }, [config]);

  return (
    <div>
      <h1>LLM Settings</h1>
      <LLMSelector
        defaultConfig={config || undefined}
        onConfigChange={setConfig}
        showAdvancedSettings={true}
      />
    </div>
  );
}
```

### API Route Integration

```tsx
// app/settings/page.tsx
'use client';

import { useState } from 'react';
import { LLMSelector } from '@/components/LLMSelector';

export default function SettingsPage() {
  const [config, setConfig] = useState(null);

  const saveSettings = async () => {
    await fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
  };

  return (
    <div>
      <LLMSelector onConfigChange={setConfig} />
      <button onClick={saveSettings} disabled={!config}>
        Save Settings
      </button>
    </div>
  );
}

// app/api/settings/route.ts
export async function POST(req: Request) {
  const config = await req.json();

  // Save to database
  await db.settings.upsert({
    where: { userId: session.userId },
    create: { userId: session.userId, llmConfig: config },
    update: { llmConfig: config }
  });

  return Response.json({ success: true });
}
```

## 🎨 Customization

### Custom Styles

```tsx
<LLMSelector
  className="my-custom-selector"
  onConfigChange={setConfig}
/>
```

```css
/* Your CSS file */
.my-custom-selector {
  background: #f9fafb;
  border: 2px solid #3b82f6;
  border-radius: 1rem;
  padding: 2rem;
}

.my-custom-selector .select {
  background: white;
  font-size: 1rem;
}

.my-custom-selector .label {
  color: #1f2937;
  font-size: 0.875rem;
  text-transform: uppercase;
}
```

### Tailwind CSS

```tsx
<LLMSelector
  className="bg-gray-50 border-2 border-blue-500 rounded-lg p-6"
  onConfigChange={setConfig}
/>
```

### Override Default Styles

The component includes default styles. To completely remove them:

```tsx
// Remove default styles
const styleEl = document.getElementById('llm-selector-styles');
if (styleEl) styleEl.remove();

// Use only your custom styles
<LLMSelector className="your-custom-class" />
```

## 🔐 Security

### Client-Side Only

The LLM Selector is a **client-side component** (`'use client'`). API keys entered are stored in component state and never sent to your server unless you explicitly do so.

### Safe Storage

**Do NOT store API keys in:**
- ❌ LocalStorage (XSS vulnerable)
- ❌ SessionStorage (XSS vulnerable)
- ❌ Cookies without httpOnly flag

**DO store API keys in:**
- ✅ Server-side environment variables
- ✅ Secure backend database (encrypted)
- ✅ Server-side session (encrypted)

### Best Practice: Server-Side Configuration

```tsx
// Client sends provider choice only
const handleConfigChange = async (config: LLMConfig) => {
  await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      provider: config.provider,
      model: config.model,
      // Don't send API keys!
    })
  });
};

// Server reads API keys from env
// app/api/chat/route.ts
export async function POST(req: Request) {
  const { provider, model } = await req.json();

  const client = createLLMClient({
    provider,
    model,
    apiKey: process.env[`${provider.toUpperCase()}_API_KEY`]
  });

  // ...
}
```

## 🎯 Provider-Specific Notes

### OpenAI
- Most reliable
- Best documentation
- Requires payment method
- $5 free credits for new accounts

### Azure OpenAI
- Enterprise SLA
- Same models as OpenAI
- Requires Azure account
- More complex setup

### Google Gemini
- **Cheapest cloud option** ($0.075/$0.30 per 1M)
- Free tier available
- Good quality
- Simpler API than OpenAI

### Anthropic Claude
- **Best reasoning**
- Longest context window
- Most expensive
- Requires AWS Bedrock

### Ollama
- **100% FREE**
- Runs locally
- Full privacy
- Requires local setup
- Slower than cloud options
- Quality varies by model size

## 📊 Pricing Displayed

The component shows pricing for each provider:

- **FREE**: Ollama (local)
- **$0.075-$0.30/1M**: Gemini (cheapest cloud)
- **$0.15-$0.60/1M**: OpenAI gpt-4o-mini (recommended)
- **$2.50-$10/1M**: OpenAI gpt-4o (best quality)
- **$3-$15/1M**: Claude 3.5 Sonnet (best reasoning)

## 🐛 Troubleshooting

### "Invalid configuration" Warning

The component validates configuration before calling `onConfigChange`. If validation fails, it passes `null`.

**Check**: Required fields for each provider
- OpenAI: `apiKey`, `model`
- Azure: `apiKey`, `azureEndpoint`, `azureDeployment`
- Gemini: `apiKey`, `model`
- Claude: `awsAccessKeyId`, `awsSecretAccessKey`, `model`
- Ollama: `model` only

### Styles Not Applying

Default styles are injected automatically. If they don't appear:

1. Check browser console for errors
2. Verify no CSP blocking inline styles
3. Try custom className instead

### TypeScript Errors

Ensure you've imported types:

```typescript
import type { LLMConfig, LLMProvider } from '@/lib/universal-llm';
```

## 📚 Related Components

- [Universal LLM Client](../../backend/universal-llm-client/README.md) - Backend client library
- [Chat Interface](../../frontend/react-chat-ui/README.md) - Pre-built chat UI
- [Streaming UI](../../frontend/streaming-ui/README.md) - Real-time response rendering

## 📄 License

MIT - Free for commercial and personal use

---

**Part of KAPI Blueprint Components** - Reusable, production-ready components for AI applications.
