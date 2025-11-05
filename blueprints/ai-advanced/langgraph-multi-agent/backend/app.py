"""
Langraph Multi-Agent System - Main Application
Production-ready multi-agent orchestration with Gradio UI

Based on Modern AI Pro Advanced Agents curriculum
"""

import os
import sys
from pathlib import Path

# Add components to path
templates_dir = Path(__file__).parents[3]
components_path = templates_dir / "components" / "backend"
sys.path.insert(0, str(components_path))

from langgraph_agent_framework.langgraph_agent import (
    LanggraphAgent,
    MultiAgentOrchestrator
)

# Universal LLM Client for multi-provider support
from universal_llm_client.python.universal_llm import (
    create_llm,
    LLMConfig,
    get_provider_info,
    list_available_providers
)
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.arxiv import ArxivQueryRun
from langchain_community.tools.polygon import (
    PolygonFinancials,
    PolygonTickerNews,
    PolygonAggregates
)
from langchain_community.tools.youtube.search import YouTubeSearchTool
import polygon
import gradio as gr
from datetime import datetime


# ============================================================================
# Configuration
# ============================================================================

# LLM Provider Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # Default to Groq (free)
LLM_MODEL = os.getenv("LLM_MODEL")  # Optional - uses provider default
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# Tool API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Validate LLM provider
if LLM_PROVIDER not in list_available_providers():
    raise ValueError(f"Invalid LLM_PROVIDER: {LLM_PROVIDER}. Must be one of: {list_available_providers()}")

# Display provider info
provider_info = get_provider_info(LLM_PROVIDER)
print(f"🤖 LLM Provider: {provider_info['name']}")
print(f"   Model: {LLM_MODEL or provider_info['default_model']}")
print(f"   Cost: {provider_info['cost']}")
print(f"   Speed: {provider_info['speed']}")


# ============================================================================
# Custom Tools
# ============================================================================

# Initialize Polygon client for stock data
stocks_client = polygon.StocksClient(POLYGON_API_KEY) if POLYGON_API_KEY else None


@tool
def get_stock_price(ticker: str) -> str:
    """
    Get current stock price for a ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

    Returns:
        Current stock price with timestamp
    """
    if not stocks_client:
        return "Stock price API not configured. Please set POLYGON_API_KEY."

    try:
        data = stocks_client.get_previous_close(ticker.upper())
        price = data[0].close
        date = data[0].timestamp
        return f"{ticker.upper()}: ${price:.2f} (as of {date})"
    except Exception as e:
        return f"Error getting stock price for {ticker}: {str(e)}"


@tool
def calculate_roi(investment: float, returns: float) -> str:
    """
    Calculate return on investment percentage.

    Args:
        investment: Initial investment amount
        returns: Final returns amount

    Returns:
        ROI percentage with interpretation
    """
    try:
        roi = ((returns - investment) / investment) * 100
        interpretation = "profit" if roi > 0 else "loss"
        return f"ROI: {roi:.2f}% ({interpretation})"
    except Exception as e:
        return f"Error calculating ROI: {str(e)}"


@tool
def get_hotel_options(location: str, checkin_date: str) -> str:
    """
    Get hotel booking options (demo implementation).

    Args:
        location: City or location name
        checkin_date: Check-in date

    Returns:
        Available hotel options
    """
    # Demo implementation
    return f"""
Available hotels in {location} for {checkin_date}:

1. **Grand Hotel** - $150/night
   - 4.5★ rating
   - Free WiFi, Pool, Gym

2. **City Inn** - $89/night
   - 4.0★ rating
   - Free WiFi, Breakfast included

3. **Luxury Suites** - $299/night
   - 5.0★ rating
   - Spa, Fine dining, Concierge
"""


@tool
def get_nasa_picture_of_day() -> str:
    """
    Get NASA's Astronomy Picture of the Day.

    Returns:
        URL and description of today's astronomy picture
    """
    try:
        from nasapy import Nasa
        nasa = Nasa()
        date = datetime.now().strftime("%Y-%m-%d")
        apod = nasa.picture_of_the_day(date, hd=True)
        return f"NASA Picture of the Day ({date}):\n{apod['title']}\n{apod['explanation']}\n\n🔗 {apod['url']}"
    except Exception as e:
        return f"Error fetching NASA picture: {str(e)}. Try visiting https://apod.nasa.gov/apod/"


# ============================================================================
# LLM Setup - Universal LLM Client
# ============================================================================

llm = create_llm(LLMConfig(
    provider=LLM_PROVIDER,
    model=LLM_MODEL,  # Will use default if None
    temperature=LLM_TEMPERATURE
))

print(f"✅ LLM initialized successfully\n")


# ============================================================================
# Specialized Agents
# ============================================================================

# Research Agent - Web search + Academic papers + YouTube
research_tools = [
    TavilySearchResults(max_results=3),
    ArxivQueryRun(),
    YouTubeSearchTool()
]

research_agent = LanggraphAgent(
    llm=llm,
    tools=research_tools,
    system_prompt="""
You are a research specialist with access to web search, academic papers, and video content.

Guidelines:
- Use web search for current events and general information
- Use ArXiv for academic/technical research
- Use YouTube search for tutorial and educational videos
- Always cite sources with URLs
- Provide comprehensive, well-structured answers
- Use markdown formatting for readability
""",
    thread_id="research",
    markdown_output=True
)

# Financial Agent - Stock data + News + Analysis tools
financial_tools = [
    get_stock_price,
    PolygonFinancials() if POLYGON_API_KEY else None,
    PolygonTickerNews() if POLYGON_API_KEY else None,
    calculate_roi
]
financial_tools = [t for t in financial_tools if t is not None]

financial_agent = LanggraphAgent(
    llm=llm,
    tools=financial_tools,
    system_prompt="""
You are a financial analyst with access to real-time stock data and financial metrics.

Guidelines:
- Use get_stock_price for current prices
- Analyze financial fundamentals when available
- Check recent news for sentiment analysis
- Calculate ROI when comparing investments
- Provide disclaimers for investment advice
- Use markdown tables for comparisons
- Include risk assessments

**Disclaimer**: This is for educational purposes only, not financial advice.
""",
    thread_id="finance",
    markdown_output=True
)

# General Assistant - Booking + NASA + Calculations
general_tools = [
    get_hotel_options,
    get_nasa_picture_of_day,
    TavilySearchResults(max_results=2)
]

general_agent = LanggraphAgent(
    llm=llm,
    tools=general_tools,
    system_prompt="""
You are a helpful general assistant for everyday tasks.

Capabilities:
- Hotel booking assistance
- NASA astronomy content
- General web search
- Helpful recommendations

Be friendly, professional, and provide detailed information.
""",
    thread_id="general",
    markdown_output=True
)


# ============================================================================
# Multi-Agent Orchestrator
# ============================================================================

orchestrator = MultiAgentOrchestrator(shared_memory=False)

orchestrator.add_agent(
    "research",
    research_agent,
    routing_keywords=["research", "paper", "study", "academic", "find", "search", "youtube", "video"]
)

orchestrator.add_agent(
    "finance",
    financial_agent,
    routing_keywords=["stock", "price", "financial", "invest", "market", "ticker", "roi", "profit"]
)

orchestrator.add_agent(
    "general",
    general_agent,
    routing_keywords=["hotel", "booking", "nasa", "picture", "space", "astronomy"]
)


# ============================================================================
# Gradio UI
# ============================================================================

def chat_with_orchestrator(message: str, history: list) -> str:
    """
    Chat function for Gradio interface with auto-routing

    Args:
        message: User input
        history: Chat history (for Gradio)

    Returns:
        Agent response with routing information
    """
    # Determine which agent will handle this
    routed_agent = orchestrator.route_to_agent(message)

    # Add routing info
    response = f"*Routing to: {routed_agent.upper()} agent*\n\n"

    # Execute with orchestrator
    for chunk in orchestrator.run(message):
        response = chunk  # Keep updating with latest

    # Add stats
    stats = orchestrator.get_orchestrator_stats()
    agent_stats = stats["agent_stats"].get(routed_agent, {})

    response += f"\n\n---\n"
    response += f"**Agent**: {routed_agent} | "
    response += f"**Invocations**: {agent_stats.get('invocations', 0)} | "
    response += f"**Total Tokens**: {agent_stats.get('total_tokens', 0)}"

    return response


# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_orchestrator,
    title="🤖 Langraph Multi-Agent System",
    description="""
**Advanced AI agent system with specialized capabilities**

Three specialized agents:
- 🔬 **Research Agent**: Web search, academic papers, YouTube videos
- 📈 **Finance Agent**: Stock prices, financial data, investment analysis
- 🌟 **General Agent**: Hotel booking, NASA astronomy, general assistance

Try these example queries:
- "Latest research on transformer models"
- "Analyze TSLA stock price"
- "Get NASA's picture of the day"
- "Compare AAPL and MSFT stocks"
- "Find hotels in San Francisco"
- "What's the ROI on $1000 investment that grew to $1500?"
    """,
    examples=[
        "Latest research on transformer models",
        "Analyze TSLA stock price",
        "Get NASA's picture of the day",
        "Compare AAPL and MSFT stocks",
        "Find hotels in San Francisco for next week",
        "Search YouTube for Python tutorials"
    ],
    theme=gr.themes.Soft()
)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting Langraph Multi-Agent System...")
    print(f"✓ Orchestrator configured with {len(orchestrator.agents)} agents")
    print(f"✓ Agents: {', '.join(orchestrator.agents.keys())}")
    print("\n🌐 Launching Gradio interface...")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
