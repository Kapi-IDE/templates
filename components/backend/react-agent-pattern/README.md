# ReAct Agent Pattern - Reusable Component

**Backend Component** - Reasoning + Acting framework for building autonomous AI agents

Based on the paper: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

## ✨ What is ReAct?

**ReAct** (Reasoning + Acting) is a framework where AI agents:
1. **Think** (reason about what to do)
2. **Act** (call tools to get information)
3. **Observe** (receive tool results)
4. **Repeat** until they have an answer

This creates agents that can solve complex multi-step problems by breaking them down into logical steps.

## 🎯 Key Features

- **Multi-step reasoning**: Agents can chain multiple tool calls
- **Tool integration**: Easy to add custom tools
- **Universal LLM support**: Works with OpenAI, Gemini, Ollama, etc.
- **Conversation memory**: Maintains context across steps
- **Debug mode**: See agent's thinking process
- **Error handling**: Graceful failure with actionable errors
- **TypeScript**: Full type safety

## 🚀 Quick Start

### Installation

```typescript
// Copy the component
cp -r components/backend/react-agent-pattern your-project/lib/

// Install dependencies
npm install
```

### Basic Usage

```typescript
import { ReActAgent, createReActPrompt } from '@/lib/react-agent';
import { createLLMClient } from '@/lib/universal-llm';

// 1. Create tools
const tools = {
  calculate: async (expr: string) => {
    return String(eval(expr));
  },

  get_time: async () => {
    return new Date().toLocaleString();
  }
};

// 2. Create system prompt
const systemPrompt = createReActPrompt({
  role: 'a helpful assistant',
  tools: {
    calculate: {
      description: 'Runs a calculation and returns the result',
      example: 'calculate: 2 + 2'
    },
    get_time: {
      description: 'Returns the current time',
      example: 'get_time:'
    }
  }
});

// 3. Create agent
const agent = new ReActAgent({
  llm: createLLMClient({
    provider: 'openai',
    apiKey: process.env.OPENAI_API_KEY,
    model: 'gpt-4o-mini'
  }),
  tools,
  systemPrompt,
  maxSteps: 10,
  debug: true
});

// 4. Run agent
const result = await agent.run('What is 15 * 7, and what time is it?');

console.log(result.answer);
// Output: "15 * 7 = 105, and the current time is 2:30 PM"

console.log(`Completed in ${result.totalSteps} steps`);
```

## 📖 How It Works

### The ReAct Loop

```
Question: "What is the stock price of Apple?"

Step 1:
  Thought: I need to get Apple's stock price
  Action: stock_price: AAPL
  PAUSE

  Observation: $185.50

Step 2:
  Thought: I have the price, I can answer now
  Answer: The current stock price of Apple (AAPL) is $185.50
```

### Agent Flow Diagram

```
User Question
     ↓
  THOUGHT: What should I do?
     ↓
  ACTION: Call a tool
     ↓
   PAUSE
     ↓
 OBSERVATION: Tool result
     ↓
  ┌─────────────┐
  │ Need more   │ Yes → Back to THOUGHT
  │ information?│
  └─────────────┘
        │ No
        ↓
     ANSWER
```

## 🛠️ Creating Custom Tools

Tools are simple async functions that take a string input and return a string output:

```typescript
const tools = {
  // Simple tool
  reverse_string: async (input: string) => {
    return input.split('').reverse().join('');
  },

  // Tool with API call
  weather: async (city: string) => {
    const response = await fetch(
      `https://api.weather.com/forecast?city=${city}`
    );
    const data = await response.json();
    return `Temperature: ${data.temp}°F, ${data.conditions}`;
  },

  // Tool with database query
  user_info: async (userId: string) => {
    const user = await prisma.user.findUnique({
      where: { id: userId }
    });
    return JSON.stringify(user);
  },

  // Tool with complex logic
  stock_analysis: async (ticker: string) => {
    const price = await getStockPrice(ticker);
    const news = await getNews(ticker);
    const sentiment = analyzeSentiment(news);

    return `${ticker}: $${price} | Sentiment: ${sentiment}`;
  }
};
```

## 📊 Real-World Examples

### Example 1: Stock Trading Agent

```typescript
import { ReActAgent, createReActPrompt } from '@/lib/react-agent';
import { getStockPrice, searchNews } from './tools';

const stockTools = {
  stock_price: async (ticker: string) => {
    const price = await getStockPrice(ticker);
    return String(price);
  },

  news_search: async (query: string) => {
    const articles = await searchNews(query);
    return articles.map(a => `${a.title}: ${a.summary}`).join('\n');
  },

  calculate: async (expr: string) => {
    return String(eval(expr.replace('result=', '')));
  }
};

const prompt = createReActPrompt({
  role: 'a stock market analyst',
  tools: {
    stock_price: {
      description: 'Get current stock price for a ticker symbol',
      example: 'stock_price: AAPL'
    },
    news_search: {
      description: 'Search for recent news about a company',
      example: 'news_search: Tesla earnings'
    },
    calculate: {
      description: 'Perform calculations',
      example: 'calculate: 10000 / 250.50'
    }
  },
  examples: `
Question: Should I buy Tesla stock?

Thought: I need Tesla's current price
Action: stock_price: TSLA
PAUSE

Observation: $250.50

Thought: Now I need recent news about Tesla
Action: news_search: Tesla
PAUSE

Observation: Tesla beats earnings... New factory opens...

Thought: News is positive. Let me calculate shares for $10,000
Action: calculate: 10000 / 250.50
PAUSE

Observation: 39.92

Answer: Based on positive news and current price of $250.50,
you could buy 39 shares with $10,000. Recommendation: BUY
  `.trim()
});

const agent = new ReActAgent({
  llm: createLLMClient({
    provider: 'groq',
    apiKey: process.env.GROQ_API_KEY,
    model: 'llama3-70b-8192'
  }),
  tools: stockTools,
  systemPrompt: prompt,
  maxSteps: 10
});

// Use the agent
const result = await agent.run('Should I invest in Microsoft?');
console.log(result.answer);
```

### Example 2: Customer Support Agent

```typescript
const supportTools = {
  lookup_order: async (orderId: string) => {
    const order = await db.orders.findUnique({ where: { id: orderId } });
    return JSON.stringify(order);
  },

  check_inventory: async (productId: string) => {
    const product = await db.products.findUnique({ where: { id: productId } });
    return `In stock: ${product.quantity}`;
  },

  create_ticket: async (issue: string) => {
    const ticket = await db.tickets.create({ data: { description: issue } });
    return `Ticket #${ticket.id} created`;
  }
};

const agent = new ReActAgent({
  llm: createLLMClient({ provider: 'openai', apiKey: '...' }),
  tools: supportTools,
  systemPrompt: createReActPrompt({
    role: 'a customer support agent',
    tools: {
      lookup_order: {
        description: 'Look up order details by order ID',
        example: 'lookup_order: ORD-12345'
      },
      check_inventory: {
        description: 'Check product availability',
        example: 'check_inventory: PROD-789'
      },
      create_ticket: {
        description: 'Create a support ticket',
        example: 'create_ticket: Customer reports damaged item'
      }
    }
  })
});

await agent.run('Order ORD-12345 is missing item PROD-789. Create a ticket.');
```

### Example 3: Research Agent

```typescript
const researchTools = {
  web_search: async (query: string) => {
    const results = await searchWeb(query);
    return results.slice(0, 5).map(r => r.snippet).join('\n\n');
  },

  read_paper: async (url: string) => {
    const content = await fetchPDF(url);
    return summarizePaper(content);
  },

  save_finding: async (text: string) => {
    await db.findings.create({ data: { content: text } });
    return 'Saved';
  }
};

const agent = new ReActAgent({
  llm: createLLMClient({ provider: 'openai', apiKey: '...' }),
  tools: researchTools,
  systemPrompt: createReActPrompt({
    role: 'a research assistant',
    tools: {
      web_search: {
        description: 'Search the web for information',
        example: 'web_search: latest AI research 2025'
      },
      read_paper: {
        description: 'Read and summarize an academic paper',
        example: 'read_paper: https://arxiv.org/pdf/2210.03629.pdf'
      },
      save_finding: {
        description: 'Save an important finding',
        example: 'save_finding: ReAct improves accuracy by 20%'
      }
    }
  })
});

await agent.run('Research the ReAct framework and save key findings');
```

## 🎨 Advanced Features

### Multi-Agent Collaboration

```typescript
const researcher = new ReActAgent({ /* ... */ });
const writer = new ReActAgent({ /* ... */ });

// Agent 1: Research
const research = await researcher.run('Find facts about climate change');

// Agent 2: Write article using research
const article = await writer.run(
  `Write an article based on: ${research.answer}`
);
```

### Conversation History

```typescript
const agent = new ReActAgent({ /* ... */ });

// First question
await agent.run('What is 2 + 2?');

// Access history
const history = agent.getHistory();
console.log(history);

// Clear for new conversation
agent.clearHistory();
```

### Debug Mode

```typescript
const agent = new ReActAgent({
  // ...
  debug: true  // Enable detailed logging
});

// Outputs:
// === Step 1 ===
// Thought: I need to get the stock price
// Action: stock_price: AAPL
// Observation: $185.50
// === Step 2 ===
// Thought: I can answer now
// Answer: The price is $185.50
```

## 🔧 Configuration Options

```typescript
interface ReActConfig {
  /** LLM client (from Universal LLM Component) */
  llm: LLMClient;

  /** Available tools the agent can use */
  tools: Record<string, Tool>;

  /** System prompt defining agent behavior */
  systemPrompt: string;

  /** Maximum reasoning steps (default: 10) */
  maxSteps?: number;

  /** Enable debug logging (default: false) */
  debug?: boolean;
}
```

## 📊 Response Format

```typescript
interface ReActResult {
  /** Final answer from the agent */
  answer: string;

  /** All reasoning steps taken */
  steps: ReActStep[];

  /** Number of steps executed */
  totalSteps: number;

  /** Whether agent succeeded */
  success: boolean;

  /** Error message if failed */
  error?: string;
}

interface ReActStep {
  step: number;
  thought: string;
  action?: string;
  actionInput?: string;
  observation?: string;
  answer?: string;
}
```

## 🐛 Error Handling

```typescript
const result = await agent.run('Complex question');

if (!result.success) {
  console.error('Agent failed:', result.error);

  // Check error type
  if (result.error === 'MAX_STEPS_EXCEEDED') {
    console.log('Agent took too many steps, try increasing maxSteps');
  } else {
    console.log('Tool execution error:', result.error);
  }

  // Review steps to see where it failed
  console.log('Steps completed:', result.steps);
}
```

## 🎯 Best Practices

### 1. Write Clear Tool Descriptions

```typescript
// ❌ Bad
calculate: {
  description: 'Does math',
  example: 'calculate: stuff'
}

// ✅ Good
calculate: {
  description: 'Performs mathematical calculations. Use Python syntax.',
  example: 'calculate: (100 * 1.5) + 25'
}
```

### 2. Provide Examples in System Prompt

```typescript
const prompt = createReActPrompt({
  role: 'an assistant',
  tools: { /* ... */ },
  examples: `
Question: What's the weather in NYC?

Thought: I need to check the weather for NYC
Action: weather: New York City
PAUSE

Observation: 72°F, Sunny

Answer: It's 72°F and sunny in New York City.
  `.trim()
});
```

### 3. Set Appropriate Max Steps

```typescript
// Simple queries
maxSteps: 5

// Complex multi-step reasoning
maxSteps: 15

// Research tasks
maxSteps: 25
```

### 4. Use Debug Mode During Development

```typescript
const agent = new ReActAgent({
  // ...
  debug: process.env.NODE_ENV === 'development'
});
```

## 🔗 Integration with Universal LLM

This component is designed to work seamlessly with the **Universal LLM Client**:

```typescript
import { createLLMClient } from '@/lib/universal-llm';
import { ReActAgent } from '@/lib/react-agent';

// Use any LLM provider
const agent = new ReActAgent({
  llm: createLLMClient({
    provider: 'ollama',  // FREE local option!
    baseURL: 'http://localhost:11434',
    model: 'llama3.2:latest'
  }),
  // ...
});
```

Supports all 5 providers: OpenAI, Azure, Gemini, Claude, Ollama

## 📚 Resources

**Papers**:
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)

**Related Components**:
- [Universal LLM Client](../universal-llm-client/README.md)
- [LLM Selector](../../frontend/llm-selector/README.md)

## 📄 License

MIT - Free for commercial and personal use

---

**Part of KAPI Blueprint Components** - Reusable, production-ready components for AI applications.
