# Universal LLM Client

**Reusable Component** - Unified interface for multiple LLM providers

## ✨ Features

- **5 LLM Providers**: OpenAI, Azure OpenAI, Gemini, Claude (Bedrock), Ollama
- **Unified Interface**: Same API for all providers
- **Auto-Detection**: Load configuration from environment variables
- **Streaming Support**: Real-time response streaming
- **Cost Tracking**: Built-in token usage and cost calculation
- **Type-Safe**: Full TypeScript support
- **Zero Lock-in**: Switch providers without code changes

## 🚀 Quick Start

### Installation

```bash
npm install openai @aws-sdk/client-bedrock-runtime
```

### Basic Usage

```typescript
import { createLLMClient } from '@/lib/universal-llm';

// Create client
const client = createLLMClient({
  provider: 'openai',
  apiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-4o-mini'
});

// Chat
const response = await client.chat({
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' }
  ]
});

console.log(response.content);
// Output: "Hello! How can I help you today?"

console.log(`Cost: $${calculateCost(response).toFixed(6)}`);
// Output: "Cost: $0.000042"
```

### Auto-Detection from Environment

```typescript
import { createLLMClientFromEnv } from '@/lib/universal-llm';

// Automatically detects provider from LLM_PROVIDER env var
const client = createLLMClientFromEnv();

const response = await client.chat({
  messages: [{ role: 'user', content: 'Explain TypeScript' }]
});
```

## 📦 Provider Setup

### OpenAI

```bash
# .env.local
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

```typescript
const client = createLLMClient({
  provider: 'openai',
  apiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-4o-mini',
  temperature: 0.7,
  maxTokens: 1000
});
```

**Models**:
- `gpt-4o-mini` - RECOMMENDED ($0.15/$0.60 per 1M tokens)
- `gpt-4o` - Best quality ($2.50/$10 per 1M tokens)
- `gpt-3.5-turbo` - Budget ($0.50/$1.50 per 1M tokens)

### Azure OpenAI

```bash
# .env.local
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=your-deployment
AZURE_OPENAI_API_VERSION=2024-02-01
```

```typescript
const client = createLLMClient({
  provider: 'azure',
  apiKey: process.env.AZURE_OPENAI_API_KEY,
  azureEndpoint: process.env.AZURE_OPENAI_ENDPOINT,
  azureDeployment: process.env.AZURE_OPENAI_DEPLOYMENT,
  azureApiVersion: '2024-02-01'
});
```

### Google Gemini

```bash
# .env.local
LLM_PROVIDER=gemini
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash-exp
```

```typescript
const client = createLLMClient({
  provider: 'gemini',
  apiKey: process.env.GEMINI_API_KEY,
  model: 'gemini-2.0-flash-exp'
});
```

**Models**:
- `gemini-2.0-flash-exp` - CHEAPEST ($0.075/$0.30 per 1M tokens)
- `gemini-1.5-pro` - Best quality ($1.25/$5 per 1M tokens)

### Anthropic Claude (AWS Bedrock)

```bash
# .env.local
LLM_PROVIDER=claude
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

```typescript
const client = createLLMClient({
  provider: 'claude',
  awsRegion: 'us-east-1',
  awsAccessKeyId: process.env.AWS_ACCESS_KEY_ID,
  awsSecretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  model: 'anthropic.claude-3-5-sonnet-20241022-v2:0'
});
```

### Ollama (FREE Local)

```bash
# Install Ollama
brew install ollama  # macOS
# or download from https://ollama.ai

# Start Ollama
ollama serve

# Pull a model
ollama pull llama3.2

# .env.local
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

```typescript
const client = createLLMClient({
  provider: 'ollama',
  baseURL: 'http://localhost:11434',
  model: 'llama3.2:latest'
});
```

**Models**:
- `llama3.2:latest` - 3B, fast, good quality
- `llama3.2:7b` - 7B, better quality
- `llama3.2:70b` - 70B, best quality (requires GPU)
- `mistral:latest` - Alternative model
- `codellama:latest` - Optimized for code

## 🎯 Usage Examples

### Basic Chat

```typescript
const response = await client.chat({
  messages: [
    { role: 'system', content: 'You are a helpful coding assistant.' },
    { role: 'user', content: 'Write a function to reverse a string in TypeScript' }
  ]
});

console.log(response.content);
```

### Streaming Responses

```typescript
for await (const chunk of client.chatStream({
  messages: [
    { role: 'user', content: 'Write a long story about AI' }
  ]
})) {
  process.stdout.write(chunk.content);

  if (chunk.done) {
    console.log('\n✅ Done!');
    break;
  }
}
```

### Multi-Turn Conversation

```typescript
const conversation: Message[] = [
  { role: 'system', content: 'You are a helpful assistant.' }
];

// First turn
conversation.push({ role: 'user', content: 'What is TypeScript?' });
let response = await client.chat({ messages: conversation });
conversation.push({ role: 'assistant', content: response.content });

// Second turn
conversation.push({ role: 'user', content: 'How is it different from JavaScript?' });
response = await client.chat({ messages: conversation });
conversation.push({ role: 'assistant', content: response.content });

console.log(response.content);
```

### Advanced Configuration

```typescript
const response = await client.chat({
  messages: [{ role: 'user', content: 'Tell me a joke' }],
  temperature: 0.9,      // More creative
  maxTokens: 100,        // Shorter response
  topP: 0.95,            // Nucleus sampling
  stopSequences: ['\n\n'] // Stop at double newline
});
```

### Cost Tracking

```typescript
import { calculateCost, getProviderPricing } from '@/lib/universal-llm';

const response = await client.chat({
  messages: [{ role: 'user', content: 'Hello!' }]
});

// Calculate cost for this response
const cost = calculateCost(response);
console.log(`Cost: $${cost.toFixed(6)}`);

// Get pricing info
const pricing = getProviderPricing('openai');
console.log(`Input: $${pricing.inputCostPer1M} per 1M tokens`);
console.log(`Output: $${pricing.outputCostPer1M} per 1M tokens`);
```

### Provider Switching

```typescript
// Switch providers without changing code
const providers: LLMProvider[] = ['openai', 'gemini', 'ollama'];

for (const provider of providers) {
  const client = createLLMClient({
    provider,
    apiKey: process.env[`${provider.toUpperCase()}_API_KEY`],
    model: getDefaultModel(provider)
  });

  const response = await client.chat({
    messages: [{ role: 'user', content: 'What is 2+2?' }]
  });

  console.log(`${provider}: ${response.content}`);
  console.log(`Cost: $${calculateCost(response).toFixed(6)}`);
}
```

## 🔒 Security Best Practices

### 1. Environment Variables

**NEVER** hardcode API keys in code:

```typescript
// ❌ BAD
const client = createLLMClient({
  provider: 'openai',
  apiKey: 'sk-proj-abc123...'  // NEVER DO THIS
});

// ✅ GOOD
const client = createLLMClient({
  provider: 'openai',
  apiKey: process.env.OPENAI_API_KEY
});
```

### 2. Separate Keys for Environments

```bash
# .env.local (development)
OPENAI_API_KEY=sk-proj-dev-key...

# .env.production (production)
OPENAI_API_KEY=sk-proj-prod-key...
```

### 3. Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'), // 10 requests per minute
});

// In your API route
const { success } = await ratelimit.limit(userId);
if (!success) {
  throw new Error('Rate limit exceeded');
}

const response = await client.chat({ messages });
```

### 4. Input Validation

```typescript
import { z } from 'zod';

const MessageSchema = z.object({
  role: z.enum(['system', 'user', 'assistant']),
  content: z.string().min(1).max(10000) // Limit message length
});

const messages = req.body.messages.map(m => MessageSchema.parse(m));
const response = await client.chat({ messages });
```

### 5. Timeout Handling

```typescript
const timeout = (ms: number) => new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Timeout')), ms)
);

try {
  const response = await Promise.race([
    client.chat({ messages }),
    timeout(30000) // 30 second timeout
  ]);
} catch (error) {
  if (error.message === 'Timeout') {
    console.error('LLM request timed out');
  }
}
```

## 💰 Pricing Comparison

| Provider | Input (per 1M) | Output (per 1M) | Best For |
|----------|----------------|-----------------|----------|
| **Ollama** | **FREE** | **FREE** | Development, privacy |
| **Gemini 2.0 Flash** | $0.075 | $0.30 | Production (cheapest) |
| OpenAI gpt-4o-mini | $0.15 | $0.60 | Production (reliable) |
| OpenAI gpt-4o | $2.50 | $10.00 | Complex reasoning |
| Azure OpenAI | $0.15-$10 | $0.60-$30 | Enterprise |
| Claude 3.5 Sonnet | $3.00 | $15.00 | Best reasoning |

**Cost Examples** (1,000 token input, 500 token output):

- Ollama: **$0** 🎉
- Gemini: **$0.000225**
- OpenAI gpt-4o-mini: **$0.000450**
- OpenAI gpt-4o: **$0.007500**
- Claude: **$0.010500**

## 🎯 Use Cases

### 1. Chatbots

```typescript
// AI Chat Interface
const client = createLLMClientFromEnv();

export async function POST(req: Request) {
  const { messages } = await req.json();

  const response = await client.chat({
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      ...messages
    ]
  });

  return Response.json(response);
}
```

### 2. Document Q&A

```typescript
// RAG with any LLM
const client = createLLMClientFromEnv();

const context = await searchDocuments(query);

const response = await client.chat({
  messages: [
    {
      role: 'system',
      content: `Answer based on this context:\n\n${context}`
    },
    { role: 'user', content: query }
  ]
});
```

### 3. Code Generation

```typescript
// SQL Query Builder
const client = createLLMClient({
  provider: 'openai',
  apiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-4o-mini',
  temperature: 0 // Deterministic for code
});

const response = await client.chat({
  messages: [
    {
      role: 'system',
      content: `Generate SQL queries. Schema:\n${schema}`
    },
    { role: 'user', content: 'Show top 10 customers by revenue' }
  ]
});
```

### 4. Data Analysis

```typescript
// Analyze CSV data
const client = createLLMClientFromEnv();

const response = await client.chat({
  messages: [
    {
      role: 'system',
      content: `Analyze this CSV data:\n${csvData}`
    },
    { role: 'user', content: 'What are the key insights?' }
  ],
  maxTokens: 2000
});
```

## 🐛 Troubleshooting

### OpenAI: "Incorrect API key"

```bash
# Verify key format
echo $OPENAI_API_KEY  # Should start with sk-proj-

# Test key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Azure: "Deployment not found"

```bash
# Verify deployment exists
az cognitiveservices account deployment list \
  --resource-group YOUR_RG \
  --name YOUR_RESOURCE
```

### Gemini: "API key not valid"

```bash
# Test key
curl "https://generativelanguage.googleapis.com/v1/models?key=$GEMINI_API_KEY"
```

### Claude: "AccessDeniedException"

```bash
# Verify Bedrock access
aws bedrock list-foundation-models --region us-east-1

# Verify model access
aws bedrock get-foundation-model \
  --model-identifier anthropic.claude-3-5-sonnet-20241022-v2:0
```

### Ollama: "Connection refused"

```bash
# Start Ollama
ollama serve

# Verify running
curl http://localhost:11434/api/version

# Pull model if needed
ollama pull llama3.2
```

## 📚 API Reference

See [lib/universal-llm.ts](lib/universal-llm.ts) for full TypeScript definitions.

## 📄 License

MIT - Free for commercial and personal use

---

**Part of KAPI Blueprint Components** - Reusable, production-ready components for AI applications.
