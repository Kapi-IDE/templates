# Universal LLM Client Integration

**Date**: October 2, 2025
**Component**: Universal LLM Client (Python)
**Blueprint**: Langraph Multi-Agent System

---

## ✅ What Was Integrated

The Langraph Multi-Agent blueprint now supports **5 LLM providers** through the Universal LLM Client component, allowing developers to easily switch between providers without code changes.

## 🎯 Benefits

### 1. **Provider Flexibility**
- Switch LLM providers via environment variable
- No code changes required
- Test different providers for cost/performance optimization

### 2. **Cost Optimization**
- Start with FREE providers (Groq, Ollama)
- Compare pricing across providers
- Built-in cost estimation

### 3. **Development to Production**
- Develop with Groq (free, fast)
- Deploy with OpenAI/Claude (reliable, powerful)
- A/B test providers in production

### 4. **Privacy Options**
- Use cloud providers for convenience
- Use Ollama for privacy-sensitive applications
- No vendor lock-in

---

## 📦 Files Created/Modified

### New Files (1)
1. `/components/backend/universal-llm-client/python/universal_llm.py` ✅
   - 450 LOC Python module
   - LangChain-compatible LLM factory
   - Support for 5 providers
   - Pricing database
   - Provider information helpers

### Modified Files (4)
1. `/blueprints/ai-advanced/langgraph-multi-agent/backend/app.py` ✅
   - Replaced hardcoded Groq client
   - Added Universal LLM Client import
   - Added provider configuration from env vars
   - Added provider info display on startup

2. `/blueprints/ai-advanced/langgraph-multi-agent/.env.example` ✅
   - Added LLM_PROVIDER configuration
   - Added LLM_MODEL override option
   - Added LLM_TEMPERATURE setting
   - Documented all 5 providers with signup URLs

3. `/blueprints/ai-advanced/langgraph-multi-agent/README.md` ✅
   - Added "Universal LLM Client" to features
   - Added provider switching documentation
   - Added provider comparison table
   - Updated component reuse section

4. `/blueprints/ai-advanced/langgraph-multi-agent/metadata.yaml` ✅
   - Added universal-llm-client-python to components_used
   - Added Ollama to llm_providers list

---

## 🔧 How It Works

### Configuration (Environment Variables)

```bash
# .env file
LLM_PROVIDER=groq  # or openai, anthropic, gemini, ollama
LLM_MODEL=llama-3.3-70b-versatile  # Optional - uses default
LLM_TEMPERATURE=0.7  # Optional - 0.0 to 1.0

# API Keys (provide for your chosen provider)
GROQ_API_KEY=gsk_your_key_here
OPENAI_API_KEY=sk-proj_your_key_here
ANTHROPIC_API_KEY=sk-ant_your_key_here
GOOGLE_API_KEY=your_key_here
# Ollama needs no API key
```

### Code Flow

```python
# 1. Import Universal LLM Client
from universal_llm_client.python.universal_llm import (
    create_llm,
    LLMConfig,
    get_provider_info
)

# 2. Load configuration from environment
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_MODEL = os.getenv("LLM_MODEL")  # None = use default
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# 3. Display provider info
provider_info = get_provider_info(LLM_PROVIDER)
print(f"Using {provider_info['name']}")
print(f"Cost: {provider_info['cost']}")

# 4. Create LLM instance
llm = create_llm(LLMConfig(
    provider=LLM_PROVIDER,
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE
))

# 5. Use with Langraph agents (no changes needed!)
agent = LanggraphAgent(
    llm=llm,  # Works with any provider
    tools=tools,
    system_prompt=prompt
)
```

---

## 🎨 Supported Providers

| Provider | Cost | Speed | Free Tier | Best For |
|----------|------|-------|-----------|----------|
| **Groq** | FREE | ⚡ Fastest | 14,400 req/day | Development, prototyping |
| **OpenAI** | $0.15-$30/1M | Fast | 200 req/day | Production, reliability |
| **Claude** | $3-$15/1M | Medium | Varies | Complex reasoning |
| **Gemini** | $0.075-$7/1M | Fast | 1,500 req/day | Cost optimization |
| **Ollama** | FREE (local) | Varies | Unlimited | Privacy, offline |

---

## 🚀 Usage Examples

### Example 1: Switch to OpenAI

```bash
# Edit .env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-proj-your_key

# Restart
python backend/app.py
```

**Output**:
```
🤖 LLM Provider: OpenAI
   Model: gpt-4o-mini
   Cost: $0.15-$30 per 1M tokens
   Speed: Fast
✅ LLM initialized successfully
```

### Example 2: Switch to Claude for Better Reasoning

```bash
# Edit .env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=sk-ant-your_key

# Restart
python backend/app.py
```

### Example 3: Use Ollama for Privacy

```bash
# 1. Install Ollama
brew install ollama

# 2. Start Ollama server
ollama serve

# 3. Pull model
ollama pull llama3.2

# 4. Edit .env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2:latest

# 5. Start app (no API key needed!)
python backend/app.py
```

### Example 4: Use Gemini for Cost Optimization

```bash
# Edit .env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-exp
GOOGLE_API_KEY=your_key

# 50% cheaper than OpenAI!
```

---

## 💰 Pricing Comparison

### Scenario: 10M input tokens, 2M output tokens per month

| Provider | Monthly Cost | Notes |
|----------|--------------|-------|
| **Groq** | **$0** | FREE tier covers this usage |
| **Gemini** | **$1.35** | Cheapest cloud option |
| **OpenAI (GPT-4o-mini)** | **$2.70** | 2x Gemini cost |
| **Claude** | **$60** | Premium for reasoning |
| **Ollama** | **$0** | Local, but requires hardware |

### Recommendation by Use Case

| Use Case | Recommended Provider | Reason |
|----------|---------------------|---------|
| Development/Testing | **Groq** | Fast, free, no limits for dev |
| MVP/Prototype | **Groq** or **Gemini** | Free or very cheap |
| Production (Cost) | **Gemini** | 50% cheaper than OpenAI |
| Production (Reliable) | **OpenAI** | Most stable, best docs |
| Complex Reasoning | **Claude** | Best performance |
| Privacy-Critical | **Ollama** | Local, no data leaves server |

---

## 🔍 Component API

### `create_llm(config: LLMConfig)`

Create a LangChain-compatible LLM instance.

```python
llm = create_llm(LLMConfig(
    provider='groq',           # Required
    model='llama-3.3-70b',     # Optional - uses default
    temperature=0.7,           # Optional - default 0.7
    max_tokens=None,           # Optional
    streaming=False            # Optional
))
```

### `get_provider_info(provider: str)`

Get information about a provider.

```python
info = get_provider_info('groq')
print(info['name'])         # "Groq"
print(info['cost'])         # "FREE"
print(info['speed'])        # "Fastest"
print(info['signup_url'])   # "https://console.groq.com/keys"
```

### `list_available_providers()`

List all supported providers.

```python
providers = list_available_providers()
# ['groq', 'openai', 'anthropic', 'gemini', 'ollama']
```

### `estimate_cost(provider, model, input_tokens, output_tokens)`

Estimate cost for a request.

```python
cost = estimate_cost('openai', 'gpt-4o-mini', 10000, 2000)
print(f"${cost:.4f}")  # "$0.0027"
```

---

## 📊 Advantages Over Direct Integration

### Before (Direct Groq)

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)
```

**Problems**:
- ❌ Locked to single provider
- ❌ Must change code to switch
- ❌ No pricing information
- ❌ No provider comparison

### After (Universal LLM Client)

```python
from universal_llm_client.python.universal_llm import create_llm, LLMConfig

llm = create_llm(LLMConfig(
    provider=os.getenv("LLM_PROVIDER", "groq"),
    temperature=0.7
))
```

**Benefits**:
- ✅ Switch via environment variable
- ✅ No code changes needed
- ✅ Built-in pricing database
- ✅ Provider information helpers
- ✅ Easy A/B testing

---

## 🎯 Next Steps

### Potential Enhancements

1. **Add More Providers**
   - Cohere
   - Together AI
   - Replicate

2. **Advanced Features**
   - Automatic fallback on rate limits
   - Load balancing across providers
   - Cost-based routing
   - Performance monitoring

3. **UI Integration**
   - Provider selector in Gradio UI
   - Live cost tracking
   - Provider comparison dashboard

4. **Enterprise Features**
   - Azure OpenAI support
   - AWS Bedrock integration
   - Custom model endpoints

---

## ✅ Testing

### Test Provider Switching

```bash
# Test each provider
LLM_PROVIDER=groq python backend/app.py
LLM_PROVIDER=openai python backend/app.py
LLM_PROVIDER=anthropic python backend/app.py
LLM_PROVIDER=gemini python backend/app.py
LLM_PROVIDER=ollama python backend/app.py
```

### Test Default Behavior

```bash
# Should default to Groq
unset LLM_PROVIDER
python backend/app.py
```

### Test Model Override

```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o python backend/app.py
```

---

## 📄 Related Documentation

- **Universal LLM Client Component**: `/components/backend/universal-llm-client/python/`
- **Langraph Agent Framework**: `/components/backend/langgraph-agent-framework/`
- **Blueprint README**: `/blueprints/ai-advanced/langgraph-multi-agent/README.md`

---

**Built with KAPI** - Component reuse for faster development

**Universal LLM Client** - Switch providers, not code
