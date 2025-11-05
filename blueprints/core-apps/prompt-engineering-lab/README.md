# Prompt Engineering Lab

**Core App #26** - Version control for prompts with A/B testing, temperature testing, and cost tracking.

Perfect tool for optimizing LLM prompts before deploying to production.

## ✨ Features

- **Multi-Provider Support**: Test prompts across 5 LLM providers (OpenAI, Azure, Gemini, Claude, Ollama)
- **Prompt Versioning**: Git-style version control for prompts
- **A/B Testing**: Compare multiple prompt variations side-by-side
- **Parameter Testing**: Test different temperatures, max tokens, top_p values
- **Cost Tracking**: Real-time cost calculation per prompt test
- **Response Quality Rating**: Track which prompts perform best
- **Prompt Library**: Save and organize successful prompts
- **Export/Import**: Share prompts with team members
- **Diff View**: See exactly what changed between prompt versions
- **Test Suites**: Run multiple test cases against a prompt
- **FREE Option**: Use Ollama locally with zero API costs

## 🚀 Quick Start (22 minutes)

### Prerequisites
- Node.js 18+
- Database (PostgreSQL recommended, or use Vercel Postgres)
- LLM Provider (Start with FREE Ollama, upgrade when needed)

### FREE Setup (Ollama - No API Keys)

```bash
# 1. Install Ollama
brew install ollama  # macOS
# or download from https://ollama.ai

# 2. Start Ollama
ollama serve

# 3. Pull a model
ollama pull llama3.2

# 4. Clone/copy this directory
cd prompt-engineering-lab

# 5. Install dependencies
npm install

# 6. Configure environment
cp .env.example .env.local

# 7. Edit .env.local
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
DATABASE_URL=postgresql://postgres:password@localhost:5432/prompt_lab

# 8. Setup database
npx prisma db push

# 9. Start app
npm run dev
```

Visit http://localhost:3000 - **Completely FREE!**

### Production Setup (OpenAI)

```bash
# 1-6. Same as above

# 7. Edit .env.local
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
DATABASE_URL=postgresql://...

# 8-9. Same as above
```

## 🔐 LLM Provider Setup

### Option 1: Ollama (FREE - RECOMMENDED FOR BEGINNERS)

**Cost**: ❌ **FREE**

**Setup**:
```bash
# Install
brew install ollama

# Start
ollama serve

# Pull model
ollama pull llama3.2

# Configure
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

**Pros**:
- ✅ Completely FREE
- ✅ No API keys needed
- ✅ Full privacy
- ✅ No rate limits
- ✅ Works offline

**Cons**:
- ❌ Slower than cloud APIs
- ❌ Quality depends on model size
- ❌ Requires local resources

### Option 2: OpenAI (MOST RELIABLE)

**Cost**: $0.15-$30 per 1M tokens

**Setup**:
1. Sign up: https://platform.openai.com/signup
2. Add payment method: https://platform.openai.com/account/billing
3. Create API key: https://platform.openai.com/api-keys
4. Configure:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

**Models**:
- `gpt-4o-mini` - RECOMMENDED ($0.15/$0.60 per 1M)
- `gpt-4o` - Best quality ($2.50/$10 per 1M)
- `gpt-3.5-turbo` - Budget ($0.50/$1.50 per 1M)

### Option 3: Google Gemini (CHEAPEST CLOUD)

**Cost**: $0.075-$7 per 1M tokens (50% cheaper than OpenAI!)

**Setup**:
1. Get API key: https://makersuite.google.com/app/apikey
2. Configure:
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash-exp
```

### Option 4: Azure OpenAI (ENTERPRISE)

**Cost**: Same as OpenAI

For Azure setup, see [.env.example](.env.example)

### Option 5: Anthropic Claude (BEST REASONING)

**Cost**: $3-$15 per 1M tokens

For Claude/Bedrock setup, see [.env.example](.env.example)

## 💰 Pricing & Cost Tracking

### Cost Per Prompt Test

**Typical test** (100 tokens input, 200 tokens output):

| Provider | Cost Per Test | 100 Tests | 1,000 Tests |
|----------|---------------|-----------|-------------|
| **Ollama** | **FREE** | **FREE** | **FREE** 🎉 |
| **Gemini** | $0.000068 | $0.0068 | $0.068 |
| OpenAI gpt-4o-mini | $0.000135 | $0.0135 | $0.135 |
| OpenAI gpt-4o | $0.002250 | $0.225 | $2.25 |
| Claude 3.5 Sonnet | $0.003300 | $0.330 | $3.30 |

### Built-In Cost Tracking

The app automatically tracks:
- Cost per prompt test
- Total cost by provider
- Total cost by prompt
- Cost trends over time
- Alerts when exceeding budget

**Example Dashboard**:
```
Total Spent: $0.47
Ollama:      $0.00 (145 tests)
Gemini:      $0.12 (68 tests)
OpenAI:      $0.35 (42 tests)

Budget Alert: Off (Threshold: $10.00)
```

## 🎯 Core Features

### 1. Prompt Versioning

**Git-style version control for prompts:**

```
v1.0 (2025-01-15):
  "Write a blog post about {topic}"

v1.1 (2025-01-16):
  "Write an engaging blog post about {topic}.
   Use a friendly, conversational tone."

v1.2 (2025-01-17):
  "Write an engaging 500-word blog post about {topic}.
   Use a friendly, conversational tone.
   Include 3 key takeaways."
```

**Features**:
- Track all changes with timestamps
- Rollback to previous versions
- Diff view between versions
- Branch prompts for A/B testing
- Tag successful versions

### 2. A/B Testing

**Compare prompt variations side-by-side:**

| Variant A | Variant B |
|-----------|-----------|
| "Summarize this in 3 sentences" | "Create a concise 3-sentence summary" |
| Response: ... | Response: ... |
| Rating: 4.2/5 | Rating: 4.7/5 ⭐ |
| Cost: $0.0001 | Cost: $0.0001 |

**Statistical Analysis**:
- Sample size tracking
- Win rate calculation
- Confidence intervals
- Recommendations based on data

### 3. Parameter Testing

**Test different LLM parameters:**

| Temperature | Response Quality | Creativity | Consistency |
|-------------|------------------|------------|-------------|
| 0.0 | High | Low | Very High |
| 0.3 | High | Medium | High |
| 0.7 | Medium | High | Medium |
| 1.0 | Medium | Very High | Low |

**Test Matrix**:
- Temperature: 0.0 → 2.0
- Max Tokens: 100 → 4000
- Top P: 0.1 → 1.0
- Presence Penalty: -2.0 → 2.0
- Frequency Penalty: -2.0 → 2.0

### 4. Test Suites

**Run multiple test cases against a prompt:**

```typescript
const testSuite = {
  prompt: "Explain {concept} to a {level} student",
  tests: [
    { concept: "quantum physics", level: "5th grade" },
    { concept: "machine learning", level: "beginner" },
    { concept: "blockchain", level: "business executive" }
  ]
};

// Run all tests
const results = await runTestSuite(testSuite);

// Aggregate results
// - Average quality: 4.5/5
// - Total cost: $0.0042
// - Success rate: 100%
```

### 5. Response Quality Rating

**Rate responses on multiple dimensions:**

- **Accuracy**: Does it answer correctly?
- **Completeness**: Does it cover all aspects?
- **Clarity**: Is it easy to understand?
- **Conciseness**: Is it appropriately brief?
- **Tone**: Does it match the desired voice?

**Aggregate Scoring**:
```
Overall: 4.3/5 ⭐⭐⭐⭐☆
├─ Accuracy:     4.8/5
├─ Completeness: 4.5/5
├─ Clarity:      4.2/5
├─ Conciseness:  3.9/5
└─ Tone:         4.2/5
```

### 6. Prompt Library

**Organize successful prompts by category:**

```
📁 Blog Writing
  ├─ SEO-optimized articles
  ├─ Tutorial posts
  └─ Listicles

📁 Code Generation
  ├─ Python functions
  ├─ SQL queries
  └─ React components

📁 Data Analysis
  ├─ CSV summarization
  ├─ Trend analysis
  └─ Report generation

📁 Customer Support
  ├─ Email responses
  ├─ FAQ answers
  └─ Ticket categorization
```

## 🏗️ Architecture

```
prompt-engineering-lab/
├── app/
│   ├── page.tsx                    # Dashboard
│   ├── prompts/
│   │   ├── [id]/page.tsx           # Prompt editor
│   │   └── new/page.tsx            # Create prompt
│   ├── ab-test/
│   │   └── [id]/page.tsx           # A/B test view
│   ├── library/page.tsx            # Prompt library
│   └── api/
│       ├── prompts/route.ts        # CRUD operations
│       ├── test/route.ts           # Run prompt tests
│       ├── compare/route.ts        # A/B testing
│       └── export/route.ts         # Export prompts
├── components/
│   ├── PromptEditor.tsx            # Monaco editor for prompts
│   ├── ParameterTuner.tsx          # Slider controls
│   ├── ResponseViewer.tsx          # Display LLM responses
│   ├── CostTracker.tsx             # Real-time cost display
│   ├── VersionHistory.tsx          # Git-style version list
│   ├── ABTestView.tsx              # Side-by-side comparison
│   └── LLMSelector.tsx             # Provider selection (REUSED)
├── lib/
│   ├── universal-llm.ts            # Multi-provider client (REUSED)
│   ├── prompt-versioning.ts        # Version control logic
│   ├── ab-testing.ts               # Statistical analysis
│   └── cost-calculator.ts          # Cost tracking
└── prisma/
    └── schema.prisma               # Database schema
```

## 🎯 Use Cases

### 1. Optimize Customer Support Responses

**Problem**: Generic AI responses lack empathy

**Solution**: A/B test prompts with different tones

```
❌ Bad Prompt:
"Respond to this customer complaint: {complaint}"

✅ Good Prompt (after testing):
"You are a friendly customer support agent.
Acknowledge the customer's frustration, apologize sincerely,
and provide a clear solution. Keep the tone warm and professional.

Customer complaint: {complaint}"

Result: 85% satisfaction improvement
```

### 2. Code Generation Accuracy

**Problem**: AI generates code with bugs

**Solution**: Test prompts with different specificity levels

```
Temperature Testing:
  0.0 (deterministic): 95% accuracy ⭐
  0.3 (slightly creative): 92% accuracy
  0.7 (balanced): 78% accuracy
  1.0 (very creative): 61% accuracy

Conclusion: Use temperature=0.0 for code generation
```

### 3. Cost Optimization

**Problem**: Production prompts are too expensive

**Solution**: Test across providers and optimize

```
Original: OpenAI gpt-4o
  Cost per query: $0.0023
  Monthly cost (10K queries): $23.00

Optimized: Gemini 2.0 Flash
  Cost per query: $0.0007
  Monthly cost (10K queries): $7.00

Savings: 70% ($16/month)
Quality: 95% equivalent
```

## 🔒 Security Best Practices

### 1. API Key Management

```bash
# ✅ CORRECT - Server-side only
# .env.local (never committed)
OPENAI_API_KEY=sk-proj-...

# ❌ WRONG - Client-side exposure
# Don't expose API keys to browser
```

### 2. Cost Alerts

```bash
# Set alert threshold
COST_ALERT_THRESHOLD=10.00
ALERT_EMAIL=admin@company.com

# Get email when total cost exceeds $10
```

### 3. Rate Limiting

```bash
# Prevent abuse
RATE_LIMIT_PER_HOUR=100
MAX_PROMPTS_PER_USER=1000
```

### 4. Prompt Access Control

```typescript
// Restrict prompt visibility
const prompt = await prisma.prompt.findFirst({
  where: {
    id: params.id,
    OR: [
      { userId: session.userId },
      { isPublic: true }
    ]
  }
});
```

## 🚢 Production Deployment

### Vercel (Recommended)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Set environment variables
vercel env add LLM_PROVIDER
vercel env add OPENAI_API_KEY
vercel env add DATABASE_URL

# 5. Deploy to production
vercel --prod
```

### Railway

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize
railway init

# 4. Add PostgreSQL
railway add

# 5. Set variables
railway variables set LLM_PROVIDER=openai
railway variables set OPENAI_API_KEY=sk-proj-...

# 6. Deploy
railway up
```

## 🐛 Troubleshooting

### "Invalid LLM Configuration"

**Problem**: LLM provider not configured correctly

**Solution**:
```bash
# Check environment variables
echo $LLM_PROVIDER
echo $OPENAI_API_KEY

# Verify API key works
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### "Database Connection Failed"

**Problem**: Can't connect to PostgreSQL

**Solution**:
```bash
# Test connection string
psql "$DATABASE_URL"

# Check if database exists
psql -l

# Run migrations
npx prisma db push
```

### "Ollama Connection Refused"

**Problem**: Can't connect to Ollama

**Solution**:
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/version

# Pull model if needed
ollama pull llama3.2
```

## 📊 Example Workflow

### 1. Create a New Prompt

```
1. Click "New Prompt"
2. Name: "Blog Post Generator"
3. Category: "Content Writing"
4. Prompt:
   "Write a {length}-word blog post about {topic}.
    Use a {tone} tone.
    Include {sections} sections."
5. Test Cases:
   - length: 500, topic: "AI", tone: "professional", sections: 3
   - length: 800, topic: "productivity", tone: "casual", sections: 5
6. Save
```

### 2. Test Parameters

```
1. Open prompt
2. Click "Test Parameters"
3. Create test matrix:
   Temperature: [0.3, 0.5, 0.7, 0.9]
   Max Tokens: [500, 1000, 1500]
4. Run all combinations
5. View results
6. Select best: temp=0.7, maxTokens=1000
```

### 3. A/B Test Variations

```
Variant A:
"Write a blog post about {topic}"

Variant B:
"Write an engaging blog post about {topic}.
 Include real-world examples."

Run 30 tests each
Results:
  A: 4.2/5 avg rating
  B: 4.7/5 avg rating ⭐ WINNER

Winner: Variant B (p < 0.05)
```

### 4. Deploy to Production

```
1. Tag winning prompt: "v1.0-production"
2. Export as JSON
3. Import into production app
4. Monitor cost and quality
```

## 🎯 KAPI Methodology

This blueprint follows **Backwards Build**:

1. ✅ **Specification**: Prompt versioning with A/B testing and cost tracking
2. ✅ **Architecture**: Reuses Universal LLM Client + React components
3. ✅ **Implementation**: Clean separation of concerns
4. ✅ **Quality Gates**: Cost alerts, rate limiting, validation

**Component Reuse**:
- ✅ Universal LLM Client (backend)
- ✅ LLM Selector (frontend)
- ✅ React Hook Form + Zod (forms)
- ✅ PostgreSQL + Prisma (database)

**Token Savings**: ~75% by reusing existing components

## 📚 Resources

**LLM Providers**:
- [OpenAI Docs](https://platform.openai.com/docs)
- [Gemini Docs](https://ai.google.dev/docs)
- [Ollama Docs](https://ollama.ai/docs)

**Prompt Engineering**:
- [OpenAI Prompt Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)

## 📄 License

MIT - Free for commercial and personal use

---

**Built with KAPI** - Stop vibe coding. Start engineering.
