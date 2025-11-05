"""
Langraph Multi-Agent Framework Component
Based on Modern AI Pro Advanced Agents curriculum
Provides reusable patterns for building production-ready multi-agent systems with Langraph
"""

from typing import Any, Callable, Dict, List, Optional, TypedDict
from datetime import datetime
import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig


class AgentState(TypedDict):
    """State schema for multi-agent coordination"""
    messages: List[Any]
    current_agent: str
    metadata: Dict[str, Any]
    tools_used: List[str]
    total_tokens: int


class LanggraphAgent:
    """
    Base Langraph agent with ReAct pattern, tool calling, and memory management.

    Features:
    - Tool registration and execution
    - Streaming responses
    - Memory/checkpoint management
    - Token usage tracking
    - Multi-turn conversations
    - Gradio-compatible output

    Usage:
        agent = LanggraphAgent(
            llm=ChatGroq(model="llama-3.3-70b-versatile"),
            tools=[search_tool, calculator_tool],
            system_prompt="You are a helpful assistant"
        )

        for response in agent.stream("What's the weather?"):
            print(response)
    """

    def __init__(
        self,
        llm: Any,
        tools: List[Any],
        system_prompt: str = "",
        thread_id: str = "default",
        enable_memory: bool = True,
        markdown_output: bool = True
    ):
        """
        Initialize Langraph agent

        Args:
            llm: LangChain LLM instance (ChatGroq, ChatOpenAI, etc.)
            tools: List of LangChain tools (@tool decorated functions)
            system_prompt: System instructions for agent behavior
            thread_id: Conversation thread ID for memory isolation
            enable_memory: Whether to enable conversation memory
            markdown_output: Format output as markdown for Gradio
        """
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt
        self.thread_id = thread_id
        self.markdown_output = markdown_output

        # Setup memory checkpoint
        self.memory = MemorySaver() if enable_memory else None

        # Create ReAct agent executor
        self.agent_executor = create_react_agent(
            self.llm,
            self.tools,
            checkpointer=self.memory,
            state_modifier=self.system_prompt
        )

        # Configuration for thread management
        self.config = {"configurable": {"thread_id": self.thread_id}}

        # Tracking
        self.total_tokens_used = 0
        self.last_tool_used = None
        self.last_query = None

    def stream(self, message: str) -> Any:
        """
        Stream agent responses with tool usage tracking

        Args:
            message: User input message

        Yields:
            Response chunks with token usage and tool information
        """
        tokens_used = 0
        tool_name = None
        query = None

        for chunk in self.agent_executor.stream(
            {"messages": [HumanMessage(content=message)]},
            self.config
        ):
            agent_data = chunk.get("agent", None)

            if agent_data is not None:
                messages = agent_data.get("messages", None)

                if messages is not None and len(messages) > 0:
                    msg = messages[0]

                    # Extract tool calls
                    tool_calls = msg.additional_kwargs.get("tool_calls", None)

                    if tool_calls is not None and len(tool_calls) > 0:
                        tool_name = tool_calls[0].get("function", {}).get("name", None)
                        arguments_str = tool_calls[0].get("function", {}).get("arguments", '{}')

                        try:
                            arguments = json.loads(arguments_str)
                            query = arguments.get("query", None)
                        except json.JSONDecodeError:
                            query = None

                    # Extract token usage safely
                    response_metadata = getattr(msg, 'response_metadata', {})
                    token_usage = response_metadata.get('token_usage', {})
                    tokens_used = token_usage.get('total_tokens', 0)

                    self.total_tokens_used += tokens_used
                    self.last_tool_used = tool_name
                    self.last_query = query

                    # Format output
                    response = msg.content

                    if self.markdown_output:
                        # Add metadata as markdown
                        if tokens_used > 0:
                            response += f"\n\n**Tokens used**: {tokens_used}"
                        if tool_name:
                            response += f"\n\n**Tool**: {tool_name}"
                        if query:
                            response += f"\n\n**Query**: {query}"

                    yield response

    def chat(self, message: str, history: Optional[List] = None) -> str:
        """
        Single-turn chat (non-streaming) compatible with Gradio ChatInterface

        Args:
            message: User input
            history: Chat history (for Gradio compatibility)

        Returns:
            Complete response string
        """
        response = ""
        for chunk in self.stream(message):
            response = chunk  # Keep latest complete response
        return response

    def reset_memory(self):
        """Clear conversation memory for current thread"""
        self.memory = MemorySaver()
        self.agent_executor = create_react_agent(
            self.llm,
            self.tools,
            checkpointer=self.memory,
            state_modifier=self.system_prompt
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get agent usage statistics"""
        return {
            "total_tokens_used": self.total_tokens_used,
            "last_tool_used": self.last_tool_used,
            "last_query": self.last_query,
            "thread_id": self.thread_id,
            "tools_available": [t.name for t in self.tools]
        }


class MultiAgentOrchestrator:
    """
    Orchestrate multiple specialized Langraph agents

    Features:
    - Agent routing based on task type
    - Shared memory across agents
    - Agent handoff and delegation
    - Unified monitoring

    Usage:
        orchestrator = MultiAgentOrchestrator()
        orchestrator.add_agent("research", research_agent)
        orchestrator.add_agent("analysis", analysis_agent)

        response = orchestrator.run("Analyze AAPL stock")
    """

    def __init__(self, shared_memory: bool = True):
        """
        Initialize multi-agent orchestrator

        Args:
            shared_memory: Whether agents share conversation memory
        """
        self.agents: Dict[str, LanggraphAgent] = {}
        self.shared_memory = shared_memory
        self.routing_rules: Dict[str, Callable] = {}
        self.agent_stats: Dict[str, Dict] = {}

    def add_agent(
        self,
        agent_id: str,
        agent: LanggraphAgent,
        routing_keywords: Optional[List[str]] = None
    ):
        """
        Register an agent with the orchestrator

        Args:
            agent_id: Unique identifier for agent
            agent: LanggraphAgent instance
            routing_keywords: Keywords to route tasks to this agent
        """
        self.agents[agent_id] = agent
        self.agent_stats[agent_id] = {"invocations": 0, "total_tokens": 0}

        if routing_keywords:
            for keyword in routing_keywords:
                self.routing_rules[keyword.lower()] = agent_id

    def route_to_agent(self, message: str) -> str:
        """
        Determine which agent should handle the message

        Args:
            message: User input

        Returns:
            agent_id to handle the request
        """
        message_lower = message.lower()

        # Check routing rules
        for keyword, agent_id in self.routing_rules.items():
            if keyword in message_lower:
                return agent_id

        # Default to first agent
        return list(self.agents.keys())[0] if self.agents else None

    def run(self, message: str, agent_id: Optional[str] = None) -> Any:
        """
        Execute message with appropriate agent

        Args:
            message: User input
            agent_id: Optional specific agent to use (otherwise routes automatically)

        Yields:
            Agent response chunks
        """
        if agent_id is None:
            agent_id = self.route_to_agent(message)

        if agent_id not in self.agents:
            yield f"Error: Agent '{agent_id}' not found"
            return

        agent = self.agents[agent_id]
        self.agent_stats[agent_id]["invocations"] += 1

        for response in agent.stream(message):
            yield response

        # Update stats
        stats = agent.get_stats()
        self.agent_stats[agent_id]["total_tokens"] = stats["total_tokens_used"]

    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get statistics for all agents"""
        return {
            "agents": list(self.agents.keys()),
            "agent_stats": self.agent_stats,
            "total_agents": len(self.agents),
            "shared_memory": self.shared_memory
        }


# ============================================================================
# Helper Functions for Common Tools
# ============================================================================

def create_custom_tool(
    name: str,
    description: str,
    func: Callable
) -> Any:
    """
    Create a custom tool from a function

    Args:
        name: Tool name
        description: Tool description for LLM
        func: Function to execute

    Returns:
        LangChain tool
    """
    @tool(name=name, description=description)
    def custom_tool_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return custom_tool_wrapper


def create_api_tool(
    name: str,
    description: str,
    api_endpoint: str,
    api_key: Optional[str] = None,
    method: str = "GET"
) -> Any:
    """
    Create a tool that calls an external API

    Args:
        name: Tool name
        description: Tool description
        api_endpoint: API URL
        api_key: Optional API key
        method: HTTP method

    Returns:
        LangChain tool
    """
    import requests

    @tool(name=name, description=description)
    def api_tool(query: str) -> str:
        """Call external API"""
        try:
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            if method == "GET":
                response = requests.get(
                    api_endpoint,
                    params={"query": query},
                    headers=headers,
                    timeout=30
                )
            else:
                response = requests.post(
                    api_endpoint,
                    json={"query": query},
                    headers=headers,
                    timeout=30
                )

            response.raise_for_status()
            return response.text

        except Exception as e:
            return f"API error: {str(e)}"

    return api_tool
