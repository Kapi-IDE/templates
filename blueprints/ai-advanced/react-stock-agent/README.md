# ReAct Stock Trading Agent

**AI Advanced #28** - Autonomous trading agent using ReAct (Reasoning + Acting) framework

Based on Modern AI Pro curriculum - Learn AI agents through hands-on stock analysis.

## ✨ Features

### Core Capabilities
- **ReAct Framework**: Thought → Action → Observation → Answer loop
- **Multi-Step Reasoning**: Agent chains tool calls to solve complex queries
- **3 Powerful Tools**:
  - 📈 **Stock Price**: Real-time prices via Polygon.io
  - 📰 **News Search**: Sentiment analysis via DuckDuckGo
  - 🧮 **Calculator**: Python-style math for shares/returns
- **Trading Signals**: BUY/SELL/HOLD recommendations
- **Multi-Provider LLM**: OpenAI, Gemini, Claude, Groq, or FREE Ollama
- **Paper Trading**: Simulated trades for learning
- **Free to Start**: $0 using Groq + Polygon free tier

### Example Queries
```
"Should I buy Tesla stock?"
"Compare Apple and Microsoft - which is better?"
"How many shares of NVIDIA can I buy with $10,000?"
"Is Amazon a good investment based on recent news?"
```

## 🚀 Quick Start (30 minutes)

### FREE Setup (Groq + Polygon.io)

```bash
# 1. Clone/copy this directory
cd react-stock-agent

# 2. Install dependencies
npm install

# 3. Get FREE API keys

# Groq (FREE - Fast LLM)
# 1. Go to https://console.groq.com/
# 2. Sign in with Google/GitHub
# 3. Create API key: https://console.groq.com/keys
# 4. Copy key (starts with gsk_)

# Polygon.io (FREE - Stock data)
# 1. Go to https://polygon.io/
# 2. Click "Get Free API Key"
# 3. Sign up and verify email
# 4. Copy API key from dashboard

# 4. Configure environment
cp .env.example .env.local

# Edit .env.local:
GROQ_API_KEY=gsk_your-key-here
POLYGON_API_KEY=your-polygon-key
LLM_PROVIDER=groq

# 5. Start app
npm run dev
```

Visit http://localhost:3000 and start asking about stocks!

## 🔐 LLM Provider Setup

This agent uses the **Universal LLM Client** - you can choose ANY provider:

### Option 1: Groq (RECOMMENDED - Fast & FREE)

**Cost**: ❌ **FREE**
**Speed**: ⚡ Fastest inference available
**Limit**: 14,400 requests/day

```bash
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama3-70b-8192
```

**Setup**:
1. Go to https://console.groq.com/keys
2. Sign in with Google/GitHub
3. Create API key
4. Paste above

### Option 2: OpenAI (Most Reliable)

**Cost**: $0.15-$30 per 1M tokens

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

### Option 3: Google Gemini (Cheapest Cloud)

**Cost**: $0.075-$7 per 1M tokens (50% cheaper than OpenAI!)

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash-exp
```

### Option 4: Ollama (100% FREE Local)

**Cost**: ❌ **FREE**

```bash
# Install Ollama
brew install ollama

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2

# Configure
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

### Option 5: Anthropic Claude (Best Reasoning)

**Cost**: $3-$15 per 1M tokens

```bash
LLM_PROVIDER=claude
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

**All 5 providers supported via Universal LLM Component!**

## 📊 Stock Data API Setup

### Polygon.io (Stock Prices)

**Required for stock price data**

**Free Tier**:
- 5 API calls/minute
- Previous day's closing prices
- Perfect for learning!

**Setup**:
1. Go to https://polygon.io/
2. Click "Get Free API Key"
3. Sign up with email
4. Verify email
5. Copy API key from dashboard
6. Add to `.env.local`:

```bash
POLYGON_API_KEY=your-key-here
```

**Paid Plans** (optional):
- Starter: $29/month (unlimited calls)
- Developer: $99/month (real-time data)

### DuckDuckGo News (NO API KEY!)

News search works **out of the box** - no API key needed!

The agent uses DuckDuckGo to search for recent news articles about stocks.

## 💰 Pricing Breakdown

### Minimum Cost (RECOMMENDED)

- **Groq**: FREE (14,400 requests/day)
- **Polygon.io**: FREE (5 calls/min)
- **DuckDuckGo**: FREE
- **Total**: **$0/month** 🎉

**Perfect for**:
- Learning AI agents
- Educational use
- Personal stock research
- Testing strategies

### Production Use

- **Groq**: FREE
- **Polygon Starter**: $29/month
- **DuckDuckGo**: FREE
- **Total**: **$29/month**

**Perfect for**:
- Automated trading alerts
- Portfolio management
- Client advisory services

## 🎯 How It Works - The ReAct Loop

### Example: "Should I buy Tesla stock?"

```
Step 1:
  THOUGHT: I need Tesla's current stock price
  ACTION: stock_price: TSLA
  PAUSE

  OBSERVATION: 250.50

Step 2:
  THOUGHT: Now I need recent news about Tesla
  ACTION: ddgs_news: Tesla
  PAUSE

  OBSERVATION: Tesla beats Q4 earnings expectations...
                New Gigafactory announced in Texas...
                Tesla stock upgraded by analysts...

Step 3:
  THOUGHT: News is positive. Let me calculate shares for $10,000
  ACTION: calculate: 10000 / 250.50
  PAUSE

  OBSERVATION: 39.92

Step 4:
  THOUGHT: I have all the information needed
  ANSWER: Based on the current price of $250.50 and positive
          recent news (earnings beat, new factory, analyst upgrades),
          Tesla shows strong momentum.

          RECOMMENDATION: BUY

          You could purchase 39 shares with $10,000 investment.
```

### The ReAct Pattern

This agent uses **ReAct** (Reasoning + Acting):

1. **Thought**: Agent reasons about what to do
2. **Action**: Agent calls a tool (stock_price, news, calculate)
3. **Pause**: Agent waits for result
4. **Observation**: Tool returns data
5. **Repeat** until agent can answer

Based on: [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)

## 🛠️ The Three Tools

### 1. Stock Price Tool

**Source**: Polygon.io API

```typescript
Action: stock_price: AAPL
Observation: 185.50
```

**Returns**: Current closing price for any ticker symbol

### 2. News Search Tool

**Source**: DuckDuckGo (no API key needed!)

```typescript
Action: ddgs_news: Microsoft
Observation: Microsoft reports strong Azure growth...
             AI investments paying off...
             Stock reaches new high...
```

**Returns**: Latest 5 news articles with titles and summaries

**Agent performs sentiment analysis** on news to determine BUY/SELL/HOLD

### 3. Calculator Tool

**Python-style calculations**

```typescript
Action: calculate: (10000 / 250.50) * 1.15
Observation: 45.91
```

**Supports**:
- Basic math: `+`, `-`, `*`, `/`
- Parentheses: `(100 + 50) / 2`
- Math functions: `Math.sqrt(16)`, `Math.pow(2, 8)`

## 🏗️ Architecture

```
react-stock-agent/
├── app/
│   ├── page.tsx                    # Main UI with LLM Selector
│   ├── api/
│   │   ├── agent/route.ts          # ReAct agent endpoint
│   │   └── paper-trade/route.ts    # Simulated trades
│   └── components/
│       ├── AgentChat.tsx           # Chat interface
│       ├── LLMSelector.tsx         # Provider selection (REUSED)
│       ├── ThinkingProcess.tsx     # Show agent's reasoning
│       └── TradeRecommendation.tsx # BUY/SELL/HOLD display
├── lib/
│   ├── react-agent.ts              # ReAct framework (REUSED)
│   ├── universal-llm.ts            # Multi-provider LLM (REUSED)
│   └── stock-agent.ts              # Stock-specific agent
├── tools/
│   ├── stock-tools.ts              # 3 tools implementation
│   └── paper-trading.ts            # Simulated trading
└── prisma/
    └── schema.prisma               # Trade history storage
```

## 📱 User Interface

### Chat Interface

```
┌────────────────────────────────────────────────┐
│ Stock Trading Agent                            │
│                                                │
│ ⚙️ Settings                                    │
│ ┌────────────────────────────────────────┐    │
│ │ LLM Provider: [Groq ▼]                 │    │
│ │ Model: llama3-70b-8192                 │    │
│ │ Paper Trading: ✓ Enabled               │    │
│ └────────────────────────────────────────┘    │
│                                                │
│ 💬 Chat                                        │
│ ┌────────────────────────────────────────┐    │
│ │ You: Should I buy Tesla?               │    │
│ │                                        │    │
│ │ 🤖 Agent:                              │    │
│ │                                        │    │
│ │ 💭 Thinking...                         │    │
│ │ Step 1: Getting Tesla stock price      │    │
│ │ Step 2: Searching recent news          │    │
│ │ Step 3: Calculating shares             │    │
│ │                                        │    │
│ │ 📊 Analysis Complete                   │    │
│ │                                        │    │
│ │ Current Price: $250.50                 │    │
│ │ Sentiment: Positive (8/10)             │    │
│ │                                        │    │
│ │ ✅ RECOMMENDATION: BUY                 │    │
│ │                                        │    │
│ │ With $10,000 you can buy:              │    │
│ │ 39 shares @ $250.50 = $9,769.50        │    │
│ │                                        │    │
│ │ Key News:                              │    │
│ │ • Q4 earnings beat expectations        │    │
│ │ • New Gigafactory announced            │    │
│ │ • Analyst upgrades to "Strong Buy"     │    │
│ └────────────────────────────────────────┘    │
│                                                │
│ [Type your question...]              [Ask →]  │
└────────────────────────────────────────────────┘
```

### LLM Provider Selector (Reused Component!)

The UI includes the **LLM Selector** component, allowing users to:
- ✅ Switch between 5 LLM providers
- ✅ Configure API keys
- ✅ Select models
- ✅ Adjust temperature/tokens
- ✅ See pricing information

**No code needed** - just include the component!

## 🎓 Educational Value

This blueprint teaches:

### 1. ReAct Framework
- How agents reason and act
- Multi-step problem decomposition
- Tool orchestration

### 2. LLM Integration
- Using multiple LLM providers
- Prompt engineering for agents
- Cost optimization

### 3. API Integration
- Stock market data APIs
- News search APIs
- Error handling

### 4. Real-World Application
- Stock analysis workflow
- Sentiment analysis
- Trading recommendations

## ⚠️ Disclaimer

**NOT FINANCIAL ADVICE**

This is an **educational tool** for learning AI agents:

- ✅ Learn ReAct framework
- ✅ Experiment with prompts
- ✅ Understand AI reasoning
- ✅ Practice with paper trading

**NOT for**:
- ❌ Real trading decisions
- ❌ Financial advice
- ❌ Investment recommendations

**Always**:
- Consult licensed financial advisors
- Do your own research
- Understand risks before investing

## 🚀 Production Deployment

### Vercel (Recommended)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Set environment variables
vercel env add LLM_PROVIDER
vercel env add GROQ_API_KEY
vercel env add POLYGON_API_KEY

# 4. Deploy to production
vercel --prod
```

### Railway

```bash
railway init
railway variables set LLM_PROVIDER=groq
railway variables set GROQ_API_KEY=gsk_...
railway variables set POLYGON_API_KEY=...
railway up
```

## 🐛 Troubleshooting

### "Invalid Groq API Key"

```bash
# Verify key format (should start with gsk_)
echo $GROQ_API_KEY

# Test key
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

### "Polygon API rate limit"

**Free tier**: 5 calls/minute

**Solutions**:
1. Add delay between requests
2. Cache stock prices
3. Upgrade to Starter plan ($29/month)

### "No news found"

**DuckDuckGo sometimes blocks bots**

**Solutions**:
1. Add random delay: `await sleep(Math.random() * 2000)`
2. Use alternative: NewsAPI.org (requires API key)
3. Retry with backoff

### "Agent not giving recommendations"

**Check**:
1. System prompt includes BUY/SELL/HOLD instructions
2. maxSteps is high enough (try 10-15)
3. LLM has enough reasoning capability (use llama3-70b or gpt-4o-mini)

## 📊 Example Interactions

### Example 1: Single Stock Analysis

```
User: Is NVIDIA a good buy?

Agent:
  Step 1: Getting NVIDIA stock price...
  Current price: $875.50

  Step 2: Searching recent news...
  • NVIDIA announces new AI chips
  • Q4 revenue up 265% YoY
  • Major cloud partnerships

  Step 3: Sentiment analysis...
  Overall sentiment: Very Positive (9/10)

  RECOMMENDATION: BUY

  Strong fundamentals, positive news momentum.
  With $10,000: 11 shares @ $875.50
```

### Example 2: Stock Comparison

```
User: Compare Apple and Microsoft

Agent:
  Step 1: Getting prices...
  AAPL: $185.50
  MSFT: $420.75

  Step 2: Analyzing news...

  Apple:
  • iPhone 15 sales strong
  • Services revenue growth
  • Sentiment: Positive (7/10)

  Microsoft:
  • Azure AI surge
  • Record cloud revenue
  • OpenAI partnership
  • Sentiment: Very Positive (9/10)

  RECOMMENDATION: BUY MSFT

  Microsoft shows stronger momentum with AI/cloud growth.
  With $10,000:
  - AAPL: 53 shares
  - MSFT: 23 shares
```

### Example 3: Portfolio Allocation

```
User: I have $50,000 to invest. Split between AAPL, GOOGL, MSFT

Agent:
  Step 1: Getting prices...
  AAPL: $185.50
  GOOGL: $140.25
  MSFT: $420.75

  Step 2: Analyzing all three...
  [News analysis for each]

  Step 3: Calculating optimal split...

  RECOMMENDATION:

  Conservative portfolio split:
  • AAPL: 30% = $15,000 = 80 shares
  • GOOGL: 35% = $17,500 = 124 shares
  • MSFT: 35% = $17,500 = 41 shares

  Reasoning: Diversified across tech giants,
  heavier weight to GOOGL/MSFT due to AI momentum.
```

## 🎯 KAPI Methodology

This blueprint follows **Backwards Build**:

1. ✅ **Specification**: ReAct agent for stock analysis
2. ✅ **Architecture**: Reuses ReAct Component + Universal LLM
3. ✅ **Implementation**: 3 tools + agent orchestration
4. ✅ **Quality Gates**: Paper trading, error handling

**Component Reuse** (75% token savings!):
- ✅ ReAct Agent Pattern (NEW reusable component)
- ✅ Universal LLM Client (backend)
- ✅ LLM Selector (frontend)
- ✅ React Hook Form + Zod (forms)

**Based on**: Modern AI Pro curriculum notebook

## 📚 Resources

**ReAct Framework**:
- [Original Paper](https://arxiv.org/abs/2210.03629)
- [LangChain ReAct](https://python.langchain.com/docs/modules/agents/agent_types/react)

**APIs**:
- [Groq Docs](https://console.groq.com/docs)
- [Polygon.io Docs](https://polygon.io/docs)

**Related Components**:
- [ReAct Agent Pattern](../../components/backend/react-agent-pattern/README.md)
- [Universal LLM Client](../../components/backend/universal-llm-client/README.md)
- [LLM Selector](../../components/frontend/llm-selector/README.md)

## 📄 License

MIT - Free for educational and personal use

**Educational use only - not financial advice**

---

**Built with KAPI** - Stop vibe coding. Start engineering.

**Based on Modern AI Pro** - Professional AI curriculum
