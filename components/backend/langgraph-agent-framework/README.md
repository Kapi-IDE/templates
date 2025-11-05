# Langraph Agent Framework Component

**Reusable component for building production-ready multi-agent systems with Langraph**

Based on Modern AI Pro Advanced Agents curriculum.

## Overview

This component provides a battle-tested framework for building multi-agent AI systems using Langraph with the ReAct pattern. It handles the complex orchestration, memory management, tool calling, and monitoring so you can focus on agent logic.

## Features

### Core Capabilities
- ✅ **ReAct Pattern**: Reasoning + Acting loop with tool execution
- ✅ **Memory Management**: Conversation persistence with checkpointing
- ✅ **Tool Orchestration**: Dynamic tool calling with parameter extraction
- ✅ **Streaming Responses**: Real-time output for better UX
- ✅ **Token Tracking**: Monitor usage and costs
- ✅ **Multi-Agent Coordination**: Route tasks to specialized agents
- ✅ **Gradio Integration**: Drop-in compatibility with Gradio ChatInterface

### Production Features
- Thread-safe conversation management
- Error handling and graceful degradation
- Markdown formatting for UI
- Agent performance monitoring
- Tool usage analytics
- Memory reset capabilities

## Quick Start

### Basic Single Agent

```python
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph_agent import LanggraphAgent

# Setup LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key="your-key")

# Setup tools
tools = [
    TavilySearchResults(max_results=3)
]

# Create agent
agent = LanggraphAgent(
    llm=llm,
    tools=tools,
    system_prompt="You are a helpful research assistant",
    thread_id="user-123"
)

# Stream responses
for response in agent.stream("What's the latest on AI agents?"):
    print(response)
```

### Multi-Agent System

```python
from langgraph_agent import LanggraphAgent, MultiAgentOrchestrator
from langchain_core.tools import tool

# Define specialized tools
@tool
def get_stock_price(ticker: str) -> str:
    """Get current stock price"""
    # ... implementation
    return f"${price}"

@tool
def analyze_financials(ticker: str) -> str:
    """Analyze company financials"""
    # ... implementation
    return analysis

# Create specialized agents
research_agent = LanggraphAgent(
    llm=llm,
    tools=[search_tool, news_tool],
    system_prompt="You are a market research specialist"
)

analysis_agent = LanggraphAgent(
    llm=llm,
    tools=[get_stock_price, analyze_financials],
    system_prompt="You are a financial analyst"
)

# Orchestrate agents
orchestrator = MultiAgentOrchestrator(shared_memory=True)
orchestrator.add_agent(
    "research",
    research_agent,
    routing_keywords=["news", "search", "find"]
)
orchestrator.add_agent(
    "analysis",
    analysis_agent,
    routing_keywords=["analyze", "financials", "price"]
)

# Auto-routing based on keywords
for response in orchestrator.run("Analyze AAPL stock price"):
    print(response)  # Routes to analysis_agent
```

### Gradio Integration

```python
import gradio as gr
from langgraph_agent import LanggraphAgent

agent = LanggraphAgent(
    llm=llm,
    tools=tools,
    markdown_output=True  # Enable markdown formatting
)

# Option 1: Streaming
demo = gr.ChatInterface(
    fn=agent.chat,  # Single-turn chat method
    title="AI Agent Assistant"
)

# Option 2: Custom with statistics
def chat_with_stats(message, history):
    response = agent.chat(message, history)
    stats = agent.get_stats()
    return f"{response}\n\n---\n**Tokens**: {stats['total_tokens_used']}"

demo = gr.ChatInterface(
    fn=chat_with_stats,
    title="AI Agent with Stats"
)

demo.launch()
```

## Architecture

### Agent Flow

```
User Input
    ↓
Langraph Agent (ReAct)
    ↓
[Thought] → [Action] → [Tool Call] → [Observation]
    ↓
Repeat until answer
    ↓
Final Response
```

### Multi-Agent Flow

```
User Input
    ↓
MultiAgentOrchestrator
    ↓
Route to Agent (by keywords)
    ↓
Specialized Agent → Tool Execution
    ↓
Aggregate Stats
    ↓
Response
```

## API Reference

### LanggraphAgent

#### `__init__(llm, tools, system_prompt, thread_id, enable_memory, markdown_output)`

Initialize agent

**Parameters:**
- `llm` (Any): LangChain LLM instance
- `tools` (List[Any]): List of LangChain tools
- `system_prompt` (str): Agent behavior instructions
- `thread_id` (str): Conversation thread ID
- `enable_memory` (bool): Enable conversation memory (default: True)
- `markdown_output` (bool): Format as markdown (default: True)

#### `stream(message: str) -> Iterator[str]`

Stream agent responses with tool tracking

**Yields:** Response chunks with metadata

#### `chat(message: str, history: Optional[List] = None) -> str`

Single-turn chat (Gradio compatible)

**Returns:** Complete response string

#### `reset_memory()`

Clear conversation memory

#### `get_stats() -> Dict`

Get agent usage statistics

**Returns:**
```python
{
    "total_tokens_used": int,
    "last_tool_used": str,
    "last_query": str,
    "thread_id": str,
    "tools_available": List[str]
}
```

### MultiAgentOrchestrator

#### `__init__(shared_memory: bool = True)`

Initialize orchestrator

#### `add_agent(agent_id, agent, routing_keywords)`

Register agent with routing rules

**Parameters:**
- `agent_id` (str): Unique agent identifier
- `agent` (LanggraphAgent): Agent instance
- `routing_keywords` (List[str]): Keywords to route to this agent

#### `run(message, agent_id=None) -> Iterator[str]`

Execute with appropriate agent

**Parameters:**
- `message` (str): User input
- `agent_id` (str): Optional specific agent (otherwise auto-routes)

**Yields:** Agent responses

#### `get_orchestrator_stats() -> Dict`

Get all agent statistics

## Common Tools

### Built-in LangChain Tools

```python
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.arxiv import ArxivQueryRun
from langchain_community.tools.polygon import PolygonFinancials
from langchain_community.tools.youtube.search import YouTubeSearchTool

tools = [
    TavilySearchResults(max_results=2),      # Web search
    ArxivQueryRun(),                         # Academic papers
    PolygonFinancials(),                     # Stock financials
    YouTubeSearchTool()                      # YouTube search
]
```

### Custom Tools

```python
from langchain_core.tools import tool

@tool
def calculate_roi(investment: float, returns: float) -> str:
    """Calculate return on investment percentage"""
    roi = ((returns - investment) / investment) * 100
    return f"ROI: {roi:.2f}%"

@tool
def get_weather(location: str) -> str:
    """Get current weather for location"""
    # API call here
    return f"Weather in {location}: Sunny, 72°F"
```

### Helper Functions

```python
from langgraph_agent import create_custom_tool, create_api_tool

# Create tool from function
def my_function(query: str) -> str:
    return f"Processed: {query}"

my_tool = create_custom_tool(
    name="my_processor",
    description="Process user queries",
    func=my_function
)

# Create API tool
api_tool = create_api_tool(
    name="external_api",
    description="Call external service",
    api_endpoint="https://api.example.com/data",
    api_key="your-key",
    method="POST"
)
```

## LLM Provider Support

### Groq (Fast & Free)

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)
```

### OpenAI

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### Anthropic Claude

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

### Google Gemini

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

## Best Practices

### 1. System Prompts

Be specific about agent behavior:

```python
system_prompt = """
You are a financial research assistant.

Guidelines:
- Cite sources for all financial data
- Include disclaimers for investment advice
- Use markdown formatting for readability
- Show your reasoning step-by-step

When analyzing stocks:
1. Check current price
2. Review recent news
3. Analyze financials
4. Provide risk assessment
"""
```

### 2. Tool Design

Keep tools focused and well-documented:

```python
@tool
def get_stock_price(ticker: str) -> str:
    """
    Get current stock price for a ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

    Returns:
        Current price with timestamp
    """
    # Implementation
    return f"{ticker}: ${price} (as of {timestamp})"
```

### 3. Error Handling

Handle tool failures gracefully:

```python
@tool
def risky_operation(param: str) -> str:
    """Operation that might fail"""
    try:
        result = external_api_call(param)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}. Please try again or contact support."
```

### 4. Memory Management

Reset memory for new conversations:

```python
# New user session
agent = LanggraphAgent(llm, tools, thread_id=f"user-{user_id}")

# Reset for fresh start
agent.reset_memory()
```

### 5. Token Monitoring

Track costs in production:

```python
def monitored_chat(message: str) -> str:
    response = agent.chat(message)
    stats = agent.get_stats()

    if stats["total_tokens_used"] > 100000:
        log_warning(f"High token usage: {stats}")

    return response
```

## Examples

### Example 1: Research Assistant

```python
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.arxiv import ArxivQueryRun

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

tools = [
    TavilySearchResults(max_results=3),
    ArxivQueryRun()
]

agent = LanggraphAgent(
    llm=llm,
    tools=tools,
    system_prompt="You are a research assistant. Cite sources and provide academic references."
)

for response in agent.stream("Latest research on transformer models"):
    print(response)
```

### Example 2: Financial Analyst

```python
from langchain_community.tools.polygon import PolygonFinancials, PolygonTickerNews
import polygon

stocks_client = polygon.StocksClient(os.getenv("POLYGON_API_KEY"))

@tool
def get_stock_price(ticker: str) -> str:
    """Get latest stock price"""
    data = stocks_client.get_previous_close(ticker)
    return f"{ticker}: ${data['close']}"

tools = [
    get_stock_price,
    PolygonFinancials(),
    PolygonTickerNews()
]

agent = LanggraphAgent(
    llm=llm,
    tools=tools,
    system_prompt="You are a financial analyst. Provide data-driven insights."
)

for response in agent.stream("Analyze TSLA stock"):
    print(response)
```

### Example 3: Customer Support

```python
@tool
def check_order_status(order_id: str) -> str:
    """Check order status"""
    # Query database
    return f"Order {order_id}: Shipped, arriving tomorrow"

@tool
def process_refund(order_id: str) -> str:
    """Process refund request"""
    # Business logic
    return f"Refund initiated for order {order_id}"

tools = [check_order_status, process_refund]

agent = LanggraphAgent(
    llm=llm,
    tools=tools,
    system_prompt="You are a customer support agent. Be helpful and professional."
)

for response in agent.stream("I need to return order #12345"):
    print(response)
```

## Dependencies

```txt
langchain>=0.1.0
langchain-core>=0.1.0
langchain-groq>=0.1.0  # or langchain-openai, langchain-anthropic
langgraph>=0.1.0
```

## Related Components

- [Universal LLM Client](../universal-llm-client/) - Multi-provider LLM abstraction
- [ReAct Agent Pattern](../react-agent-pattern/) - TypeScript ReAct implementation
- [Agent Framework](../agent-framework/) - Base agent foundation

## License

MIT - Free for commercial and personal use

---

**Built with KAPI** - Reusable components for production AI systems
