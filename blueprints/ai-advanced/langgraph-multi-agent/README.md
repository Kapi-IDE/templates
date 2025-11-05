# Langraph Multi-Agent System

**Production-ready multi-agent AI system using Langraph with ReAct pattern, specialized agents, and automatic routing**

Based on Modern AI Pro Advanced Agents curriculum - Build intelligent systems that orchestrate multiple specialized AI agents to solve complex tasks.

## ✨ Features

### Core Capabilities
- 🤖 **3 Specialized Agents**: Research, Finance, and General assistance
- 🔄 **Automatic Routing**: Keywords-based routing to appropriate agent
- 🧠 **ReAct Pattern**: Reasoning + Acting loop with tool execution
- 💬 **Gradio Chat UI**: Beautiful web interface out-of-the-box
- 📊 **Token Tracking**: Monitor usage and costs in real-time
- 🔧 **10+ Integrated Tools**: Web search, stocks, papers, YouTube, NASA, and more
- 🎯 **Universal LLM Client**: Switch between 5 providers (Groq, OpenAI, Claude, Gemini, Ollama)

### Specialized Agents

#### 🔬 Research Agent
**Tools**: Web Search (Tavily), Academic Papers (ArXiv), YouTube Search

**Use Cases**:
- "Latest research on transformer models"
- "Find academic papers on quantum computing"
- "Search YouTube for Python tutorials"

#### 📈 Finance Agent
**Tools**: Stock Prices (Polygon), Financial Data, News, ROI Calculator

**Use Cases**:
- "What's TSLA stock price?"
- "Compare AAPL and MSFT stocks"
- "Calculate ROI on $1000 investment that grew to $1500"
- "Get latest news for NVDA ticker"

#### 🌟 General Agent
**Tools**: Hotel Booking (demo), NASA Astronomy, Web Search

**Use Cases**:
- "Get NASA's picture of the day"
- "Find hotels in San Francisco"
- "What's the weather in New York?"

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.11+
- **LLM Provider** (choose one):
  - Groq API key (RECOMMENDED - FREE, get at https://console.groq.com/keys)
  - OpenAI API key (https://platform.openai.com/api-keys)
  - Anthropic API key (https://console.anthropic.com/)
  - Google Gemini API key (https://ai.google.dev/)
  - Ollama (FREE local - https://ollama.com/)
- Tavily API key (FREE - get at https://tavily.com/)
- Polygon.io API key (FREE - get at https://polygon.io/)

### Installation

```bash
# 1. Clone or navigate to this directory
cd langgraph-multi-agent

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Configure environment variables
cp .env.example .env

# Edit .env and add your API keys:
# GROQ_API_KEY=gsk_your_key_here
# TAVILY_API_KEY=tvly_your_key_here
# POLYGON_API_KEY=your_polygon_key_here

# 4. Run the application
python backend/app.py
```

Visit **http://localhost:7860** and start chatting!

## 🔐 API Key Setup

This blueprint requires **3 API keys** (all FREE):

### 1. Groq API Key (REQUIRED - LLM Provider)

**Cost**: ❌ **FREE** (14,400 requests/day)
**Speed**: ⚡ Fastest LLM inference available

**Setup**:
1. Go to https://console.groq.com/keys
2. Sign in with Google/GitHub
3. Click "Create API Key"
4. Copy key (starts with `gsk_`)
5. Add to `.env`: `GROQ_API_KEY=gsk_your_key_here`

### 2. Tavily API Key (REQUIRED - Web Search)

**Cost**: ❌ **FREE** (1,000 searches/month)

**Setup**:
1. Go to https://tavily.com/
2. Sign up with email
3. Get API key from dashboard
4. Add to `.env`: `TAVILY_API_KEY=tvly_your_key_here`

### 3. Polygon.io API Key (REQUIRED - Stock Data)

**Cost**: ❌ **FREE** (5 calls/minute)

**Setup**:
1. Go to https://polygon.io/
2. Click "Get Free API Key"
3. Sign up and verify email
4. Copy API key from dashboard
5. Add to `.env`: `POLYGON_API_KEY=your_polygon_key_here`

### Optional APIs

**NASA API** (Optional - has default public key):
- Get at: https://api.nasa.gov/
- Add to `.env`: `NASA_API_KEY=your_key`

**Alternative LLM Providers** (Optional):
```bash
# OpenAI
OPENAI_API_KEY=sk-proj-your_key

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your_key

# Google Gemini
GOOGLE_API_KEY=your_key
```

### ⚠️ Security Best Practices

```bash
# 1. Never commit .env file
# (already in .gitignore)

# 2. Rotate API keys regularly

# 3. For production, use environment variables:
export GROQ_API_KEY="your_key"
export TAVILY_API_KEY="your_key"
export POLYGON_API_KEY="your_key"

# 4. Use secrets management (AWS Secrets Manager, etc.)
```

## 💰 Pricing Breakdown

**Total Cost**: **$0/month** for moderate usage 🎉

| Service | Free Tier | Cost After Free Tier |
|---------|-----------|---------------------|
| Groq LLM | 14,400 req/day | N/A (no paid tier yet) |
| Tavily Search | 1,000 searches/month | $0.30/1K searches |
| Polygon Stocks | 5 calls/min | $29/month unlimited |
| NASA | Unlimited | Free |

**Perfect for**:
- Learning AI agents
- Personal projects
- MVPs and prototypes
- Educational use

**For production scale**:
- Polygon Starter: $29/month (unlimited calls)
- Tavily Pro: $49/month (10K searches)
- Total: ~$78/month for heavy production use

## 🎯 How It Works - Multi-Agent Architecture

### Architecture Diagram

```
User Input
    ↓
MultiAgentOrchestrator
    ↓
Keyword-based Routing
    ↓
┌─────────────┬─────────────────┬──────────────┐
│  Research   │    Finance      │   General    │
│   Agent     │     Agent       │    Agent     │
├─────────────┼─────────────────┼──────────────┤
│• Web Search │• Stock Prices   │• Hotel       │
│• Papers     │• Financials     │• NASA        │
│• YouTube    │• News           │• Search      │
│             │• ROI Calc       │              │
└─────────────┴─────────────────┴──────────────┘
    ↓
ReAct Loop (per agent):
[Thought] → [Action] → [Tool] → [Observation] → Repeat
    ↓
Response + Stats
```

### Example Flow: "Analyze TSLA stock"

```
1. User: "Analyze TSLA stock"

2. Orchestrator routes to: FINANCE AGENT
   (detected keywords: "analyze", "stock")

3. Finance Agent ReAct Loop:

   Thought: I need the current TSLA stock price
   Action: get_stock_price("TSLA")
   Observation: TSLA: $245.50

   Thought: Now I need recent news about Tesla
   Action: PolygonTickerNews("TSLA")
   Observation: Tesla announces new Gigafactory...

   Thought: Let me get financial fundamentals
   Action: PolygonFinancials("TSLA")
   Observation: Revenue $96.7B, Profit margin 15.5%...

   Thought: I have enough data to provide analysis
   Answer: [Comprehensive analysis with price, news, fundamentals]

4. Response returned with:
   - Analysis text
   - Agent used: finance
   - Tokens used: 1,247
   - Tools used: 3
```

### Routing Logic

Keywords determine which agent handles the request:

| Keywords | Agent | Tools Available |
|----------|-------|----------------|
| research, paper, study, find, youtube, video | Research | Web search, ArXiv, YouTube |
| stock, price, financial, invest, market, ticker, roi | Finance | Stock API, Financials, News, Calculator |
| hotel, booking, nasa, picture, space | General | Hotel, NASA, Web search |

## 📱 User Interface

### Gradio Chat Interface

```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Langraph Multi-Agent System                              │
│                                                              │
│ Advanced AI agent system with specialized capabilities      │
│                                                              │
│ Three specialized agents:                                   │
│ 🔬 Research: Web search, papers, YouTube                    │
│ 📈 Finance: Stock prices, financial data                    │
│ 🌟 General: Hotel booking, NASA, general help               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ You: Analyze TSLA stock                                     │
│                                                              │
│ Agent: *Routing to: FINANCE agent*                          │
│                                                              │
│ ## TSLA Stock Analysis                                      │
│                                                              │
│ **Current Price**: $245.50                                  │
│                                                              │
│ **Recent News**:                                            │
│ • Tesla announces new Gigafactory in Mexico                 │
│ • Q4 earnings beat expectations                            │
│ • Cybertruck production ramping up                          │
│                                                              │
│ **Fundamentals**:                                           │
│ • Revenue: $96.7B (YoY +18%)                                │
│ • Profit Margin: 15.5%                                      │
│ • P/E Ratio: 45.2                                           │
│                                                              │
│ **Analysis**: Strong fundamentals with positive momentum... │
│                                                              │
│ ---                                                          │
│ Agent: finance | Invocations: 1 | Total Tokens: 1,247      │
└─────────────────────────────────────────────────────────────┘
│ [Type your message here...]                  [Send]         │
└─────────────────────────────────────────────────────────────┘
```

### Example Queries

Try these in the chat interface:

```
Research Agent:
✓ "Latest research on transformer models"
✓ "Find papers on quantum computing"
✓ "Search YouTube for Langraph tutorials"
✓ "What's new in AI research?"

Finance Agent:
✓ "What's AAPL stock price?"
✓ "Compare TSLA and NVDA stocks"
✓ "Get financial data for MSFT"
✓ "Calculate ROI: invested $5000, now worth $6500"
✓ "Latest news for GOOGL ticker"

General Agent:
✓ "Get NASA's picture of the day"
✓ "Find hotels in New York"
✓ "What's the weather today?"
✓ "Book a hotel in London"
```

## 🏗️ Blueprint Structure

```
langgraph-multi-agent/
├── backend/
│   ├── app.py                    # Main application with 3 agents
│   └── requirements.txt          # Python dependencies
├── deployment/
│   ├── Dockerfile                # Container configuration
│   └── docker-compose.yml        # Multi-service orchestration
├── .env.example                  # Environment template
├── README.md                     # This file
└── metadata.yaml                 # Blueprint metadata
```

## 🔧 Customization

### Switching LLM Providers

The blueprint uses the **Universal LLM Client** component for easy provider switching:

#### Option 1: Environment Variable (Recommended)

```bash
# Edit .env file
LLM_PROVIDER=openai  # or anthropic, gemini, ollama
OPENAI_API_KEY=sk-proj-your_key_here

# Restart app
python backend/app.py
```

#### Option 2: Programmatic

```python
from universal_llm_client.python.universal_llm import create_llm, LLMConfig

# Switch to OpenAI
llm = create_llm(LLMConfig(
    provider='openai',
    model='gpt-4o-mini',
    temperature=0.7
))

# Switch to Claude
llm = create_llm(LLMConfig(
    provider='anthropic',
    model='claude-3-5-sonnet-20241022',
    temperature=0.7
))

# Switch to Gemini (Cheapest)
llm = create_llm(LLMConfig(
    provider='gemini',
    model='gemini-2.0-flash-exp',
    temperature=0.7
))

# Switch to Ollama (FREE local)
llm = create_llm(LLMConfig(
    provider='ollama',
    model='llama3.2:latest',
    base_url='http://localhost:11434'
))
```

#### Supported Providers

| Provider | Cost | Speed | Best For |
|----------|------|-------|----------|
| **Groq** (default) | FREE | ⚡ Fastest | Development, prototyping |
| **OpenAI** | $0.15-$30/1M | Fast | Production, reliability |
| **Claude** | $3-$15/1M | Medium | Complex reasoning |
| **Gemini** | $0.075-$7/1M | Fast | Cost optimization |
| **Ollama** | FREE (local) | Varies | Privacy, offline |

### Adding a New Agent

```python
from langgraph_agent import LanggraphAgent

# Define tools for your agent
@tool
def custom_tool(param: str) -> str:
    """Your custom tool description"""
    # Implementation
    return result

# Create agent
my_agent = LanggraphAgent(
    llm=llm,
    tools=[custom_tool, search_tool],
    system_prompt="You are a specialized assistant for...",
    thread_id="my_agent"
)

# Register with orchestrator
orchestrator.add_agent(
    "my_agent",
    my_agent,
    routing_keywords=["keyword1", "keyword2"]
)
```

### Adding a New Tool

```python
from langchain_core.tools import tool

@tool
def weather_tool(location: str) -> str:
    """
    Get weather forecast for a location.

    Args:
        location: City name

    Returns:
        Weather forecast
    """
    # API call here
    response = requests.get(f"https://api.weather.com/{location}")
    return response.json()["forecast"]

# Add to existing agent
research_agent.tools.append(weather_tool)
```

### Switching LLM Providers

```python
# Change from Groq to OpenAI
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Change to Anthropic Claude
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Change to Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# 1. Set environment variables
export GROQ_API_KEY="your_key"
export TAVILY_API_KEY="your_key"
export POLYGON_API_KEY="your_key"

# 2. Build and run
docker-compose -f deployment/docker-compose.yml up -d

# 3. Access at http://localhost:7860

# 4. View logs
docker-compose logs -f

# 5. Stop
docker-compose down
```

### Using Dockerfile

```bash
# Build image
docker build -f deployment/Dockerfile -t langgraph-agent .

# Run container
docker run -p 7860:7860 \
  -e GROQ_API_KEY="your_key" \
  -e TAVILY_API_KEY="your_key" \
  -e POLYGON_API_KEY="your_key" \
  langgraph-agent
```

## 🚀 Production Deployment

### Vercel (Not recommended - use for frontend only)

Gradio apps work better on platforms with persistent connections.

### Railway (RECOMMENDED)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set GROQ_API_KEY="your_key"
railway variables set TAVILY_API_KEY="your_key"
railway variables set POLYGON_API_KEY="your_key"

# 5. Deploy
railway up
```

### Hugging Face Spaces (RECOMMENDED - FREE)

```bash
# 1. Create account at https://huggingface.co/
# 2. Create new Space (Gradio type)
# 3. Upload files:
#    - backend/app.py → app.py
#    - backend/requirements.txt → requirements.txt
# 4. Add secrets in Space settings:
#    - GROQ_API_KEY
#    - TAVILY_API_KEY
#    - POLYGON_API_KEY
# 5. Space will auto-deploy
```

### AWS / GCP / Azure

Use Docker deployment with managed container services:
- **AWS**: ECS / EKS
- **GCP**: Cloud Run / GKE
- **Azure**: Container Apps / AKS

## 🐛 Troubleshooting

### "GROQ_API_KEY not set"

```bash
# Verify environment variable
echo $GROQ_API_KEY

# Set it
export GROQ_API_KEY="gsk_your_key"

# Or add to .env file
echo "GROQ_API_KEY=gsk_your_key" >> .env
```

### "Tavily API rate limit"

Free tier: 1,000 searches/month

**Solutions**:
1. Reduce search queries
2. Upgrade to Pro plan ($49/month for 10K)
3. Use alternative search tool

### "Polygon API rate limit"

Free tier: 5 calls/minute

**Solutions**:
1. Add delay between requests
2. Cache stock prices
3. Upgrade to Starter ($29/month unlimited)

### "Agent not routing correctly"

Check routing keywords match your query:

```python
# View current routing rules
print(orchestrator.routing_rules)

# Add more keywords
orchestrator.add_agent(
    "finance",
    financial_agent,
    routing_keywords=["stock", "ticker", "price", "invest", "shares", "market"]
)
```

### "Token usage too high"

Monitor with stats:

```python
stats = orchestrator.get_orchestrator_stats()
print(stats)

# Reduce by:
# 1. Using more specific tools
# 2. Shorter system prompts
# 3. Limiting tool results
```

## 📊 Component Reuse

This blueprint uses **2 KAPI components**:

### 1. Langraph Agent Framework

Located at: `/components/backend/langgraph-agent-framework/`

**Provides**:
- `LanggraphAgent` - ReAct pattern implementation
- `MultiAgentOrchestrator` - Multi-agent coordination
- Tool registration and execution
- Memory management

**Reuse in your projects**:
```python
import sys
sys.path.insert(0, "path/to/components/backend")

from langgraph_agent_framework.langgraph_agent import (
    LanggraphAgent,
    MultiAgentOrchestrator
)
```

### 2. Universal LLM Client (Python)

Located at: `/components/backend/universal-llm-client/python/`

**Provides**:
- Multi-provider LLM support (Groq, OpenAI, Claude, Gemini, Ollama)
- Unified LangChain-compatible interface
- Pricing information and cost estimation
- Provider information and recommendations

**Reuse in your projects**:
```python
from universal_llm_client.python.universal_llm import (
    create_llm,
    LLMConfig,
    get_provider_info,
    estimate_cost
)

# Create LLM
llm = create_llm(LLMConfig(
    provider='groq',
    model='llama-3.3-70b-versatile'
))

# Get provider info
info = get_provider_info('groq')
print(f"Using {info['name']} - Cost: {info['cost']}")
```

## 🎓 Educational Value

This blueprint teaches:

### 1. Multi-Agent Systems
- Agent specialization and delegation
- Automatic routing strategies
- Shared vs independent memory

### 2. Langraph Framework
- ReAct pattern implementation
- Tool registration and calling
- Checkpoint/memory management

### 3. Production Patterns
- Error handling in agents
- Token tracking and monitoring
- Gradio UI integration
- Docker deployment

### 4. LLM Integration
- Multiple provider support
- Streaming responses
- Cost optimization

## 📚 Resources

**Langraph**:
- [Official Docs](https://python.langchain.com/docs/langgraph)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

**LangChain**:
- [Tools Catalog](https://python.langchain.com/docs/integrations/tools/)
- [LLM Providers](https://python.langchain.com/docs/integrations/llms/)

**API Documentation**:
- [Groq API](https://console.groq.com/docs)
- [Tavily Search](https://docs.tavily.com/)
- [Polygon.io](https://polygon.io/docs)

**Related Blueprints**:
- [ReAct Stock Agent](../react-stock-agent/) - Single-agent stock analysis
- [Finance Analysis](../../industry/finance-analysis/) - Production financial system

**Related Components**:
- [Langraph Agent Framework](../../../components/backend/langgraph-agent-framework/) - Reusable agent patterns
- [Universal LLM Client](../../../components/backend/universal-llm-client/) - Multi-provider LLM

## ⚠️ Disclaimer

**Educational Use Only**

This blueprint is for learning AI agent development:
- ✅ Learn Langraph and multi-agent patterns
- ✅ Experiment with tool orchestration
- ✅ Understand ReAct framework
- ✅ Build prototypes and MVPs

**NOT for**:
- ❌ Financial advice (Finance Agent is demo only)
- ❌ Medical advice
- ❌ Legal advice
- ❌ Production trading systems without proper review

**Financial Disclaimer**: Stock data and analysis are for educational purposes only. Not investment advice. Consult licensed financial advisors for investment decisions.

## 📄 License

MIT - Free for commercial and personal use

---

**Built with KAPI** - Production-ready blueprints for AI development

**Based on Modern AI Pro** - Advanced Agents curriculum
