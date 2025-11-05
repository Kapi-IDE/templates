# AI Integration Components

Production-ready AI/LLM integration components for rapid application development. All components follow security-first design with environment-based configuration.

## 🎯 Purpose

Provide standardized, secure, and production-ready integrations for major AI providers:
- **Gemini** - Google's latest models with reasoning capabilities
- **Azure OpenAI** - Enterprise-grade OpenAI models with multi-region support
- **Anthropic Claude** - Advanced reasoning models via AWS Bedrock

## 📦 Available Components

### 1. Gemini Integration (`gemini/`)

OpenAI-compatible client for Google's Gemini models with advanced features.

**Key Features:**
- OpenAI-compatible interface for easy migration
- Reasoning effort control (LOW/MEDIUM/HIGH)
- Tool/function calling support
- Text embeddings (text-embedding-004)
- Streaming responses
- Production error handling

**Quick Start:**
```python
from components.backend.ai_integrations.gemini import (
    create_gemini_client,
    chat_completion,
    ReasoningEffort
)

# Create client (uses GEMINI_API_KEY env var)
client = create_gemini_client()

# Simple completion
response = chat_completion(
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    model="gemini-2.0-flash"
)

# With reasoning effort
response = chat_completion(
    messages=[{"role": "user", "content": "Solve this complex problem..."}],
    reasoning_effort=ReasoningEffort.HIGH.value,
    model="gemini-2.5-pro-preview-05-06"
)

# Tool calling
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather in a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City, State"}
            },
            "required": ["location"]
        }
    }
}

response = chat_completion(
    messages=[{"role": "user", "content": "What's the weather in NYC?"}],
    tools=[weather_tool],
    tool_choice="auto"
)
```

**Environment Variables:**
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

**Supported Models:**
- `gemini-2.0-flash` - Fast, cost-effective
- `gemini-2.5-pro-preview-05-06` - Advanced reasoning
- `text-embedding-004` - Embeddings

---

### 2. Azure OpenAI Integration (`azure-openai/`)

Enterprise-grade OpenAI models via Azure with multi-region support and DeepSeek integration.

**Key Features:**
- Multi-region deployment support
- DeepSeek model integration
- Embeddings via LangChain
- Special model handling (o3-mini)
- Comprehensive error logging
- Production-ready retry logic

**Quick Start:**
```python
from components.backend.ai_integrations.azure_openai import (
    create_azure_openai_client,
    create_azure_embeddings_client,
    chat_completion
)

# Create client (uses env vars)
client = create_azure_openai_client()

# Chat completion
result = chat_completion(
    client=client,
    model="gpt-4",  # Your deployment name
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=500,
    temperature=0.7
)

print(result["content"])
print(f"Tokens used: {result['total_tokens']}")

# o3-mini special handling
result = chat_completion(
    client=client,
    model="o3-mini",
    messages=[{"role": "user", "content": "Solve this..."}],
    max_tokens=1000,
    is_o3_mini=True  # Omits temperature parameter
)

# Embeddings
embeddings_client = create_azure_embeddings_client()
vectors = embeddings_client.embed_query("Your text here")
```

**Environment Variables:**
```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4  # For health checks

# Azure DeepSeek (optional)
AZURE_DEEPSEEK_ENDPOINT=https://your-deepseek-endpoint.azure.com/
AZURE_DEEPSEEK_KEY=your_deepseek_key
```

**Supported Models:**
- `gpt-4` - Most capable
- `gpt-35-turbo` - Fast and cost-effective
- `o3-mini` - Specialized reasoning (special parameters)
- `deepseek-coder` - Code generation (via DeepSeek client)

---

### 3. Anthropic Claude via AWS Bedrock (`anthropic-bedrock/`)

Advanced reasoning models through AWS infrastructure with enterprise security.

**Key Features:**
- AWS Bedrock integration
- Claude 3.5 Sonnet, Haiku, and 3.7 Sonnet
- Multi-turn conversation support
- Advanced sampling controls (top_p, top_k)
- Token usage tracking
- AWS credential management

**Quick Start:**
```python
from components.backend.ai_integrations.anthropic_bedrock import (
    create_bedrock_client,
    invoke_claude,
    invoke_claude_advanced,
    ClaudeModel
)

# Create client (uses AWS credentials from environment)
client = create_bedrock_client(region="us-east-1")

# Simple completion
response = invoke_claude(
    client=client,
    prompt="Explain how LLMs work in 20 words or less",
    model_type=ClaudeModel.SONNET_3_7.value
)

# With system prompt
response = invoke_claude(
    client=client,
    prompt="Write a haiku about coding",
    model_type="3.5-sonnet",
    system_prompt="You are a creative poet",
    temperature=0.9
)

# Multi-turn conversation
messages = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "What are its main features?"}
]

response = invoke_claude_advanced(
    client=client,
    messages=messages,
    model_type="3.7-sonnet",
    max_tokens=1000
)

print(response["text"])
print(f"Stop reason: {response['stop_reason']}")
print(f"Tokens: {response['usage']}")
```

**Environment Variables:**
```bash
# AWS credentials (one of the following methods):

# Method 1: Environment variables
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Method 2: AWS credentials file (~/.aws/credentials)
# [default]
# aws_access_key_id = your_access_key
# aws_secret_access_key = your_secret_key

# Method 3: IAM role (when running on AWS infrastructure)
# No configuration needed - uses instance role
```

**Supported Models:**
- `3.5-sonnet` - Balanced performance and cost
- `3.5-haiku` - Fast and cost-effective
- `3.7-sonnet` - Latest model with enhanced reasoning

---

## 🔒 Security Best Practices

### Never Hardcode Credentials
```python
# ❌ NEVER DO THIS
api_key = "sk-1234567890abcdef"

# ✅ ALWAYS DO THIS
api_key = os.getenv("GEMINI_API_KEY")
```

### Environment Variable Management
```bash
# Development: Use .env file (never commit!)
cp .env.example .env
# Add your keys to .env

# Production: Use secure secret management
# - AWS Secrets Manager
# - Azure Key Vault
# - Google Secret Manager
# - Kubernetes Secrets
```

### Error Handling
```python
from components.backend.ai_integrations.gemini import create_gemini_client

try:
    client = create_gemini_client()
except ValueError as e:
    logger.error(f"Gemini configuration error: {e}")
    # Fallback to alternative provider or notify admin
```

---

## 🧪 Health Checks

All components include health check functions for monitoring:

```python
from components.backend.ai_integrations.gemini import gemini_health_check
from components.backend.ai_integrations.azure_openai import azure_openai_health_check
from components.backend.ai_integrations.anthropic_bedrock import bedrock_health_check

# Add to your health check endpoint
@app.get("/health")
def health_check():
    return {
        "gemini": gemini_health_check(),
        "azure_openai": azure_openai_health_check(),
        "claude_bedrock": bedrock_health_check()
    }
```

---

## 📊 Cost Optimization

### Token Usage Tracking
```python
# Azure OpenAI provides detailed usage
result = chat_completion(client, model="gpt-4", messages=[...])
print(f"Input tokens: {result['prompt_tokens']}")
print(f"Output tokens: {result['completion_tokens']}")
print(f"Total cost estimate: {result['estimated_cost']}")

# Claude Bedrock provides usage statistics
response = invoke_claude_advanced(client, messages=[...])
print(f"Usage: {response['usage']}")
```

### Model Selection Strategy
```python
# Use cheaper models for simple tasks
if task_complexity == "low":
    model = "gemini-2.0-flash"  # Fast and cheap
elif task_complexity == "medium":
    model = "gpt-35-turbo"      # Balanced
else:
    model = "claude-3.7-sonnet" # Advanced reasoning
```

---

## 🔄 Provider Switching

All components follow similar interfaces for easy switching:

```python
def get_ai_response(prompt: str, provider: str = "gemini"):
    if provider == "gemini":
        from components.backend.ai_integrations.gemini import chat_completion
        return chat_completion(
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content

    elif provider == "azure":
        from components.backend.ai_integrations.azure_openai import (
            create_azure_openai_client, chat_completion
        )
        client = create_azure_openai_client()
        return chat_completion(
            client, "gpt-4", [{"role": "user", "content": prompt}]
        )["content"]

    elif provider == "claude":
        from components.backend.ai_integrations.anthropic_bedrock import (
            create_bedrock_client, invoke_claude
        )
        client = create_bedrock_client()
        return invoke_claude(client, prompt)
```

---

## 📦 Dependencies

### Gemini
```bash
pip install openai  # For OpenAI-compatible interface
```

### Azure OpenAI
```bash
pip install azure-ai-inference azure-identity openai langchain-openai
```

### Anthropic Claude (Bedrock)
```bash
pip install boto3 botocore
```

---

## 🚀 Quick Integration Guide

### Step 1: Install Dependencies
```bash
# Install all AI integration dependencies
pip install openai azure-ai-inference azure-identity langchain-openai boto3 botocore
```

### Step 2: Configure Environment
```bash
# Create .env file
cat > .env << EOF
# Gemini
GEMINI_API_KEY=your_gemini_key

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_azure_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# AWS (for Bedrock)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=us-east-1
EOF
```

### Step 3: Import and Use
```python
# Add components to Python path
import sys
from pathlib import Path
components_path = Path(__file__).parent / "components" / "backend"
sys.path.insert(0, str(components_path))

# Import and use
from ai_integrations.gemini import chat_completion

response = chat_completion(
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## 🏗️ Architecture Patterns

### Factory Pattern for Provider Selection
```python
class AIProviderFactory:
    @staticmethod
    def get_client(provider: str):
        if provider == "gemini":
            from ai_integrations.gemini import create_gemini_client
            return create_gemini_client()
        elif provider == "azure":
            from ai_integrations.azure_openai import create_azure_openai_client
            return create_azure_openai_client()
        elif provider == "claude":
            from ai_integrations.anthropic_bedrock import create_bedrock_client
            return create_bedrock_client()
        raise ValueError(f"Unknown provider: {provider}")
```

### Retry Logic with Fallback
```python
def robust_completion(prompt: str, providers: list = ["gemini", "azure", "claude"]):
    for provider in providers:
        try:
            return get_ai_response(prompt, provider)
        except Exception as e:
            logger.warning(f"{provider} failed: {e}, trying next...")
    raise Exception("All AI providers failed")
```

---

## 📝 Component Metadata

| Component | LOC | Setup Time | Dependencies | Token Efficiency |
|-----------|-----|------------|--------------|------------------|
| Gemini | 240 | 1 min | openai | High (OpenAI compatible) |
| Azure OpenAI | 280 | 2 min | azure-ai-inference, openai | High (multi-region) |
| Anthropic Bedrock | 260 | 3 min | boto3 | High (AWS infrastructure) |

**Voice Patterns for LanceDB Discovery:**
- "AI integration", "LLM client", "Gemini setup"
- "Azure OpenAI", "Claude integration", "Bedrock client"
- "Multi-provider AI", "LLM abstraction", "AI provider switching"

---

## 🤝 Contributing

When adding new AI providers:
1. Follow the security-first pattern (environment variables only)
2. Include health check function
3. Provide usage examples in docstrings
4. Add error handling and logging
5. Update this README with integration guide

---

**Security Note**: These components contain NO hardcoded credentials, API keys, or secrets. All sensitive configuration is loaded from environment variables at runtime.
