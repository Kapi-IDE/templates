# KAPI Component Registry

Reusable, production-ready components for KAPI blueprints.

---

## Backend Components

### Universal LLM Client

**Location**: `components/backend/universal-llm-client/`

**Purpose**: Unified interface for multiple LLM providers

**Providers Supported**:
- OpenAI (GPT-4, GPT-4o, GPT-3.5)
- Azure OpenAI (Enterprise)
- Google Gemini (Cheapest cloud)
- Anthropic Claude (Best reasoning)
- Ollama (FREE local)

**Key Features**:
- Single API for all providers
- Auto-detection from environment variables
- Streaming support
- Built-in cost calculation
- Type-safe TypeScript
- Zero vendor lock-in

**Setup Time**: 5 min
**Token Savings**: 50% (vs implementing from scratch)

**Dependencies**:
```json
{
  "openai": "^4.0.0",
  "@aws-sdk/client-bedrock-runtime": "^3.0.0"
}
```

**Compatible With**:
- AI Chat Interface
- Perplexity Clone
- SQL Query Builder
- RAG Document Q&A
- Any app using LLMs

**Usage**:
```typescript
import { createLLMClient } from '@/lib/universal-llm';

const client = createLLMClient({
  provider: 'openai',
  apiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-4o-mini'
});

const response = await client.chat({
  messages: [{ role: 'user', content: 'Hello!' }]
});
```

**Pricing**:
- Ollama: FREE (local)
- Gemini: $0.075-$0.30 per 1M tokens
- OpenAI: $0.15-$30 per 1M tokens
- Azure: Same as OpenAI
- Claude: $3-$15 per 1M tokens

---

## Frontend Components

### LLM Selector

**Location**: `components/frontend/llm-selector/`

**Purpose**: React UI component for selecting and configuring LLM providers

**Key Features**:
- Interactive provider selection
- Provider-specific configuration forms
- Built-in pricing information
- Model selection dropdown
- Advanced settings (temperature, tokens)
- Compact mode
- Fully styled (customizable)

**Setup Time**: 2 min
**Token Savings**: 70% (vs building from scratch)

**Dependencies**:
```json
{
  "react": "^18.0.0"
}
```

**Compatible With**:
- Universal LLM Client (backend)
- Any React/Next.js app

**Usage**:
```tsx
import { LLMSelector } from '@/components/LLMSelector';

<LLMSelector
  onConfigChange={setConfig}
  showPricing={true}
  showModelSelection={true}
/>
```

**Props**:
- `onConfigChange` - Callback when configuration changes
- `defaultProvider` - Initial provider selection
- `showPricing` - Show cost information
- `showModelSelection` - Show model dropdown
- `showAdvancedSettings` - Temperature, max tokens, etc.
- `allowedProviders` - Limit provider options
- `compact` - Smaller UI mode

---

## Usage Examples

### Complete Chat App

See: `components/backend/universal-llm-client/examples/chat-app.tsx`

**Features Demonstrated**:
- LLMSelector for provider configuration
- Universal LLM Client for backend
- Regular and streaming responses
- Cost tracking
- Multi-turn conversations
- Settings persistence

**Code**:
```tsx
import { LLMSelector } from '@/components/LLMSelector';
import { createLLMClient } from '@/lib/universal-llm';

const [config, setConfig] = useState(null);

const sendMessage = async () => {
  const client = createLLMClient(config);
  const response = await client.chat({ messages });
  // ...
};

return (
  <div>
    <LLMSelector onConfigChange={setConfig} />
    {/* Chat UI */}
  </div>
);
```

---

## Component Composition

### AI Chat Interface Blueprint

Uses:
- ✅ Universal LLM Client
- ✅ LLM Selector
- Chat UI (separate component)

### Perplexity Clone Blueprint

Uses:
- ✅ Universal LLM Client
- ✅ LLM Selector
- Search Client (separate component)
- Chat UI (separate component)

### SQL Query Builder Blueprint

Uses:
- ✅ Universal LLM Client
- ✅ LLM Selector
- Monaco Editor (external)
- Result Table (separate component)

---

## Installation Guide

### 1. Copy Components

```bash
# Backend
cp -r components/backend/universal-llm-client your-project/lib/

# Frontend
cp components/frontend/llm-selector/LLMSelector.tsx your-project/components/
```

### 2. Install Dependencies

```bash
npm install openai @aws-sdk/client-bedrock-runtime
```

### 3. Configure Environment

```bash
# .env.local
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

### 4. Use in Your App

```tsx
import { createLLMClientFromEnv } from '@/lib/universal-llm';

const client = createLLMClientFromEnv();
```

---

## Testing

### Unit Tests

```typescript
import { createLLMClient } from '@/lib/universal-llm';

describe('Universal LLM Client', () => {
  it('should create OpenAI client', () => {
    const client = createLLMClient({
      provider: 'openai',
      apiKey: 'test-key',
      model: 'gpt-4o-mini'
    });

    expect(client.getProvider()).toBe('openai');
    expect(client.getModel()).toBe('gpt-4o-mini');
  });

  it('should chat with OpenAI', async () => {
    const client = createLLMClient({
      provider: 'openai',
      apiKey: process.env.OPENAI_API_KEY,
      model: 'gpt-4o-mini'
    });

    const response = await client.chat({
      messages: [{ role: 'user', content: 'Say "test"' }]
    });

    expect(response.content).toContain('test');
    expect(response.provider).toBe('openai');
  });
});
```

---

## Roadmap

### Planned Components

1. **Search Client** (Q1 2025)
   - Brave Search, Serper, Google, Bing
   - Unified interface like LLM Client
   - Used in Perplexity Clone

2. **Vector Store Client** (Q1 2025)
   - ChromaDB, Pinecone, Weaviate, Supabase
   - Used in RAG applications

3. **Streaming UI** (Q1 2025)
   - Real-time response rendering
   - Token-by-token display
   - Cost tracking overlay

4. **Chat UI Library** (Q2 2025)
   - Pre-built chat interface
   - Message threading
   - File attachments
   - Voice input

---

## Contributing

To add a new component:

1. Create directory: `components/{backend|frontend}/component-name/`
2. Add implementation files
3. Write comprehensive README.md
4. Create usage examples
5. Add to this registry
6. Update blueprints that can use it

---

## License

MIT - Free for commercial and personal use

---

**Version**: 1.0.0
**Last Updated**: 2025-10-02
**Total Components**: 2 (1 backend, 1 frontend)
