# Perplexity Clone

AI-powered search engine with real-time web results, citations, and follow-up questions.

**Multi-LLM Support**: Choose from 5 AI providers (including FREE local Ollama!)

**Core App #6** - Demonstrates flexible multi-provider API architecture.

## ✨ Features

- **Multiple LLM Providers**: OpenAI, Azure, Gemini, Claude, or FREE Ollama
- **Multiple Search APIs**: Brave, Serper, Google, or Bing
- **Web Search Integration**: Real-time search results with citations
- **AI-Powered Answers**: Synthesized responses from search results
- **Source Citations**: Inline citations with links
- **Follow-up Questions**: Conversational search with context
- **Streaming Responses**: Real-time answer generation
- **Related Questions**: AI-suggested follow-up queries
- **Clean UI**: Modern Perplexity.ai-inspired interface
- **Responsive Design**: Desktop and mobile support

## 🚀 Quick Start (20 minutes)

### FREE Setup (No API Keys - Ollama + Brave Free Tier)

```bash
# 1. Install Ollama (FREE local LLM)
# Download from: https://ollama.ai
# Or: brew install ollama (macOS)

# 2. Pull a model
ollama pull llama3.2

# 3. Clone/copy this directory
cd perplexity-clone

# 4. Install dependencies
npm install

# 5. Configure environment
cp .env.example .env.local

# 6. Edit .env.local:
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
SEARCH_PROVIDER=brave
BRAVE_SEARCH_API_KEY=your-free-brave-key

# 7. Start Ollama
ollama serve

# 8. Start app
npm run dev
```

Visit http://localhost:3000 - **Completely free!**

## 🔐 LLM Provider Setup (Choose ONE)

### Option 1: Ollama (FREE - RECOMMENDED FOR BEGINNERS)

**Cost**: ❌ **FREE** (runs on your computer)

#### Step 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

#### Step 2: Pull a Model

```bash
# Small, fast (3B parameters, ~2GB)
ollama pull llama3.2

# Better quality (7B parameters, ~4GB)
ollama pull llama3.2:7b

# Best quality (70B parameters, ~40GB - requires GPU)
ollama pull llama3.2:70b
```

#### Step 3: Start Ollama

```bash
ollama serve
```

#### Step 4: Configure .env.local

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

**Pros**:
- ✅ Completely FREE
- ✅ No API keys needed
- ✅ Full privacy (runs locally)
- ✅ No rate limits
- ✅ Works offline

**Cons**:
- ❌ Requires local resources (CPU/GPU)
- ❌ Slower than cloud APIs
- ❌ Quality varies by model size

---

### Option 2: OpenAI (RELIABLE - BEST FOR PRODUCTION)

**Cost**: $0.15-$30 per 1M tokens

#### Steps:
1. Sign up: https://platform.openai.com/signup
2. Add payment: https://platform.openai.com/account/billing
3. Create API key: https://platform.openai.com/api-keys
4. Add to `.env.local`:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

**Pros**:
- ✅ Most reliable
- ✅ Fast responses
- ✅ Best documentation
- ✅ Streaming support

---

### Option 3: Google Gemini (CHEAPEST CLOUD OPTION)

**Cost**: $0.075-$7 per 1M tokens (50% cheaper than OpenAI!)

#### Steps:
1. Sign up: https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env.local`:

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Uses existing component**: `/components/backend/ai-integrations/gemini/`

**Pros**:
- ✅ Cheapest cloud option
- ✅ Good quality
- ✅ Free tier available

---

### Option 4: Azure OpenAI (ENTERPRISE)

**Cost**: Same as OpenAI

#### Steps:
1. Azure Portal: https://portal.azure.com
2. Create OpenAI resource
3. Deploy model
4. Add to `.env.local`:

```bash
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=your-deployment
AZURE_OPENAI_API_VERSION=2024-02-01
```

**Uses existing component**: `/components/backend/ai-integrations/azure-openai/`

**Pros**:
- ✅ Enterprise SLA
- ✅ Data residency control
- ✅ Private networking

---

### Option 5: Anthropic Claude (BEST REASONING)

**Cost**: $3-$15 per 1M tokens

#### Steps:
1. AWS Bedrock console
2. Enable Claude models
3. Create IAM credentials
4. Add to `.env.local`:

```bash
LLM_PROVIDER=claude
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

**Uses existing component**: `/components/backend/ai-integrations/anthropic-bedrock/`

**Pros**:
- ✅ Best at reasoning
- ✅ Long context window
- ✅ High quality

---

## 🔍 Search API Setup (Choose ONE)

### Option 1: Brave Search (RECOMMENDED)

**Cost**: FREE (2,000 queries/month) or $5/month (20,000)

#### Step 1: Sign Up

1. Go to https://brave.com/search/api/
2. Click "Get Started"
3. Create account with email

#### Step 2: Choose Plan

- **Free Plan**: 2,000 queries/month
- **Pro Plan**: $5/month for 20,000 queries
- **Start with free tier** - upgrade when needed

#### Step 3: Create API Key

1. Go to dashboard: https://brave.com/search/api/dashboard
2. Click "Create API Key"
3. Copy key (starts with `BSA...`)

#### Step 4: Add to .env.local

```bash
SEARCH_PROVIDER=brave
BRAVE_SEARCH_API_KEY=BSA...
```

**Rate Limits**:
- Free: 1 request/second
- Pro: 10 requests/second

---

### Option 2: Serper.dev (CHEAPEST AT SCALE)

**Cost**: $50 for 1M queries (vs Brave $250 for 1M)

#### Steps:
1. Sign up: https://serper.dev/
2. Create API key
3. Add to `.env.local`:

```bash
SEARCH_PROVIDER=serper
SERPER_API_KEY=your-key
```

---

### Option 3: Google Custom Search

**Cost**: FREE (100/day) or $5 per 1,000 queries

#### Steps:
1. Create search engine: https://programmablesearchengine.google.com/
2. Get API key: https://developers.google.com/custom-search
3. Add to `.env.local`:

```bash
SEARCH_PROVIDER=google
GOOGLE_SEARCH_API_KEY=your-key
GOOGLE_SEARCH_ENGINE_ID=your-id
```

---

### Option 4: Bing Search API

**Cost**: FREE (1,000/month) or $3 per 1,000 queries

#### Steps:
1. Sign up: https://www.microsoft.com/en-us/bing/apis
2. Create API key
3. Add to `.env.local`:

```bash
SEARCH_PROVIDER=bing
BING_SEARCH_API_KEY=your-key
```

---

## 💰 Pricing Comparison

### LLM Providers (Per 1M Tokens)

| Provider | Input | Output | Free Tier | Notes |
|----------|-------|--------|-----------|-------|
| **Ollama** | **FREE** | **FREE** | ✅ Unlimited | Runs locally |
| **Gemini 2.0 Flash** | $0.075 | $0.30 | ✅ Yes | CHEAPEST cloud |
| OpenAI gpt-4o-mini | $0.15 | $0.60 | $5 credits | Recommended |
| OpenAI gpt-4o | $2.50 | $10.00 | $5 credits | Best quality |
| Azure OpenAI | $0.15-$10 | $0.60-$30 | ❌ No | Enterprise |
| Claude 3.5 Sonnet | $3.00 | $15.00 | ❌ No | Best reasoning |

### Search Providers

| Provider | Free Tier | Paid Pricing | Rate Limits |
|----------|-----------|--------------|-------------|
| **Brave** | 2,000/month | $5 for 20K/month | 1 req/sec (free) |
| **Serper** | 2,500 queries | $50 for 1M | No limit |
| Google Custom | 100/day | $5 per 1,000 | 10 req/sec |
| Bing | 1,000/month | $3 per 1,000 | 3 req/sec |

### Cost Per Search Examples

**Setup 1: FREE (Ollama + Brave free)**
- LLM: $0
- Search: $0 (within free tier)
- **Total**: $0 🎉

**Setup 2: Cheapest Cloud (Gemini + Brave free)**
- LLM: ~$0.0005
- Search: $0 (within free tier)
- **Total**: ~$0.0005 per search

**Setup 3: Production (OpenAI gpt-4o-mini + Serper)**
- LLM: ~$0.0009
- Search: ~$0.00005
- **Total**: ~$0.001 per search

**Setup 4: Enterprise (Azure + Brave Pro)**
- LLM: ~$0.0009
- Search: ~$0.00025
- **Total**: ~$0.0012 per search

## 🏗️ Architecture

**Component Reuse**:

```
perplexity-clone/
├── lib/
│   ├── llm-client.ts           # Universal LLM interface
│   │   └── Uses existing:
│   │       ├── /components/backend/ai-integrations/azure-openai/
│   │       ├── /components/backend/ai-integrations/gemini/
│   │       ├── /components/backend/ai-integrations/anthropic-bedrock/
│   │       └── /components/backend/node-llm-framework/ (NEW - Ollama)
│   └── search-client.ts        # Universal search interface
└── app/api/
    ├── search/route.ts         # Multi-provider search
    └── answer/route.ts         # Multi-provider LLM
```

**Unified Interface**:
All LLM providers use the same interface, making it easy to switch:

```typescript
const answer = await generateAnswer(query, searchResults, {
  provider: process.env.LLM_PROVIDER
});
```

## 🔒 Security Best Practices

### 1. Managing Multiple Optional API Keys

**Only configure what you use**:

```bash
# ✅ CORRECT - Only set what you use
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
SEARCH_PROVIDER=brave
BRAVE_SEARCH_API_KEY=BSA...

# ❌ WRONG - Don't set unused providers
# OPENAI_API_KEY=  # Not needed if using Ollama!
```

### 2. Separate Development and Production Keys

```bash
# .env.local (Development)
LLM_PROVIDER=ollama
SEARCH_PROVIDER=brave

# .env.production (Production - Vercel/Railway)
LLM_PROVIDER=gemini
GEMINI_API_KEY=prod-key-here
SEARCH_PROVIDER=serper
SERPER_API_KEY=prod-key-here
```

### 3. Ollama Security

```bash
# ✅ CORRECT - Localhost only (default)
OLLAMA_BASE_URL=http://localhost:11434

# ❌ WRONG - Never expose publicly
# OLLAMA_BASE_URL=http://0.0.0.0:11434
```

**Why**: Ollama has no authentication. Exposing it publicly allows anyone to use your compute resources.

### 4. API Key Rotation

| Provider | Dashboard | Rotation Frequency |
|----------|-----------|-------------------|
| OpenAI | https://platform.openai.com/api-keys | 90 days |
| Azure | https://portal.azure.com | 90 days |
| Gemini | https://makersuite.google.com | 90 days |
| Brave | https://brave.com/search/api/dashboard | 90 days |
| Ollama | N/A (no keys) | N/A |

### 5. Git Security

```bash
# .gitignore (already included)
.env
.env.local
.env.production

# Never commit:
git add .env  # ❌ WRONG
```

### 6. Monitor API Usage

**OpenAI**: https://platform.openai.com/usage
**Gemini**: https://console.cloud.google.com/apis/dashboard
**Brave**: https://brave.com/search/api/dashboard

**Set budget alerts** to avoid unexpected charges:
- OpenAI: Usage limits in billing settings
- Gemini: Budget alerts in Google Cloud Console
- Brave: Email alerts at 80% usage

## 🚢 Production Deployment

### Recommended Setups

**Budget ($0-5/month):**
```bash
LLM_PROVIDER=ollama  # Free (self-hosted)
SEARCH_PROVIDER=brave  # Free tier
```

**Startup ($10-20/month):**
```bash
LLM_PROVIDER=gemini  # Cheapest cloud
GEMINI_MODEL=gemini-2.0-flash-exp
SEARCH_PROVIDER=brave  # $5/month Pro
```

**Production ($50+/month):**
```bash
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
SEARCH_PROVIDER=serper  # Best cost at scale
```

**Enterprise:**
```bash
LLM_PROVIDER=azure
SEARCH_PROVIDER=brave
# + monitoring, caching, rate limiting
```

## 🐛 Troubleshooting

### Ollama Not Responding

**Problem**: Connection refused to localhost:11434

**Solution**:
```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Verify model is pulled
ollama pull llama3.2
```

### "Invalid LLM_PROVIDER" Error

**Problem**: Provider not recognized

**Solution**:
Check `.env.local` has valid provider:
```bash
LLM_PROVIDER=ollama  # or openai, azure, gemini, claude
```

### Ollama Slow Responses

**Problem**: Answers take 30+ seconds

**Solution**:
1. Use smaller model: `llama3.2` (3B) instead of `llama3.2:70b`
2. Check CPU/GPU usage
3. Close other applications
4. Consider cloud provider for better performance

## 🎯 KAPI Methodology

This blueprint follows **Backwards Build** with **component reuse**:

1. ✅ **Specification**: Multi-LLM support, flexible search, citations
2. ✅ **Architecture**: Reused `/components/backend/ai-integrations/` components
3. ✅ **Implementation**: Universal LLM + Search interfaces
4. ✅ **Quality Gates**: Multi-provider validation, fallback handling

**Component Reuse**: Leverages 4 existing AI integration components + creates unified interface.

**Token Savings**: ~65% by reusing existing LLM integrations.

## 📚 Resources

**LLM Providers**:
- [Ollama Documentation](https://ollama.ai/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Azure OpenAI Docs](https://learn.microsoft.com/azure/ai-services/openai/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Claude API Docs](https://docs.anthropic.com/)

**Search APIs**:
- [Brave Search API](https://brave.com/search/api/)
- [Serper.dev Docs](https://serper.dev/documentation)
- [Google Custom Search](https://developers.google.com/custom-search)
- [Bing Search API](https://www.microsoft.com/en-us/bing/apis)

## 📄 License

MIT License - Free for commercial and personal use

---

**Built with KAPI** - Stop vibe coding. Start engineering.
