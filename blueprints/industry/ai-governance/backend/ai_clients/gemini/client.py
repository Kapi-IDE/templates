"""
Gemini AI Integration Component

Provides production-ready Gemini API client with OpenAI-compatible interface.
Supports reasoning effort, tool calling, embeddings, and streaming.
All credentials managed via environment variables - NO HARDCODED SECRETS.

Usage:
    from components.backend.ai_integrations.gemini import create_gemini_client, ReasoningEffort

    # Create client
    client = create_gemini_client()

    # Chat completion with reasoning
    response = client.chat.completions.create(
        model="gemini-2.5-pro-preview-05-06",
        messages=[{"role": "user", "content": "Explain quantum computing"}],
        reasoning_effort=ReasoningEffort.MEDIUM.value
    )

    # Tool calling
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": "What's the weather in NYC?"}],
        tools=[weather_tool],
        tool_choice="auto"
    )
"""

import os
from enum import Enum
from typing import Optional, List, Dict, Any
from openai import OpenAI


def get_gemini_api_key() -> str:
    """Get Gemini API key from environment variable.

    Environment Variables:
        GEMINI_API_KEY: Gemini API authentication key

    Returns:
        API key string

    Raises:
        ValueError: If API key is not configured
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Gemini API key not configured. "
            "Set GEMINI_API_KEY environment variable."
        )
    return api_key


class ReasoningEffort(Enum):
    """Reasoning effort levels for Gemini models.

    Controls how much computational effort the model uses for reasoning:
    - LOW: Faster responses, less deep reasoning
    - MEDIUM: Balanced speed and reasoning depth
    - HIGH: More thorough reasoning, slower responses
    - NONE: No explicit reasoning, standard generation
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    NONE = "none"


def create_gemini_client(
    api_key: Optional[str] = None,
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
) -> OpenAI:
    """Create Gemini client with OpenAI-compatible interface.

    Args:
        api_key: Optional API key (defaults to GEMINI_API_KEY env var)
        base_url: Gemini API base URL (default: official endpoint)

    Returns:
        OpenAI client configured for Gemini

    Example:
        # Use default configuration
        client = create_gemini_client()

        # Custom API key
        client = create_gemini_client(api_key="your-key-here")
    """
    key = api_key or get_gemini_api_key()

    return OpenAI(
        api_key=key,
        base_url=base_url
    )


# Global client instance
gemini_client = create_gemini_client()


def chat_completion(
    messages: List[Dict[str, str]],
    model: str = "gemini-2.0-flash",
    temperature: float = 0.7,
    max_tokens: int = 1024,
    reasoning_effort: Optional[str] = None,
    stream: bool = False,
    tools: Optional[List[Dict]] = None,
    tool_choice: str = "auto",
    client: Optional[OpenAI] = None
) -> Any:
    """Create chat completion with Gemini.

    Args:
        messages: List of message dicts [{"role": "user", "content": "..."}]
        model: Gemini model name (default: gemini-2.0-flash)
        temperature: Sampling temperature 0.0-1.0 (default: 0.7)
        max_tokens: Maximum tokens to generate (default: 1024)
        reasoning_effort: Optional reasoning level (LOW/MEDIUM/HIGH/NONE)
        stream: Enable streaming responses (default: False)
        tools: Optional list of tool/function definitions
        tool_choice: Tool selection strategy (default: "auto")
        client: Optional custom client (defaults to global instance)

    Returns:
        Chat completion response object (or iterator if stream=True)

    Example:
        # Simple completion
        response = chat_completion(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print(response.choices[0].message.content)

        # With reasoning
        response = chat_completion(
            messages=[{"role": "user", "content": "Solve this problem..."}],
            reasoning_effort=ReasoningEffort.HIGH.value
        )

        # Streaming
        for chunk in chat_completion(
            messages=[{"role": "user", "content": "Tell me a story"}],
            stream=True
        ):
            print(chunk.choices[0].delta.content, end="")
    """
    gemini = client or gemini_client

    # Build request parameters
    params = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }

    # Add reasoning effort if specified
    if reasoning_effort:
        params["reasoning_effort"] = reasoning_effort

    # Add tools if provided
    if tools:
        params["tools"] = tools
        params["tool_choice"] = tool_choice

    return gemini.chat.completions.create(**params)


def create_embeddings(
    text: str,
    model: str = "text-embedding-004",
    client: Optional[OpenAI] = None
) -> List[float]:
    """Create text embeddings with Gemini.

    Args:
        text: Input text to embed
        model: Embedding model name (default: text-embedding-004)
        client: Optional custom client (defaults to global instance)

    Returns:
        List of embedding vector values

    Example:
        embeddings = create_embeddings("Your text here")
        print(f"Embedding dimension: {len(embeddings)}")
    """
    gemini = client or gemini_client

    response = gemini.embeddings.create(
        input=text,
        model=model
    )

    return response.data[0].embedding


def gemini_health_check() -> bool:
    """Check if Gemini client is functioning properly.

    Returns:
        True if healthy, False otherwise

    Example:
        if gemini_health_check():
            print("Gemini is ready")
    """
    try:
        # Simple test completion
        response = chat_completion(
            messages=[{"role": "user", "content": "Say 'OK'"}],
            max_tokens=10
        )
        return bool(response.choices[0].message.content)
    except Exception:
        return False


# Tool/Function calling helper
def create_tool_definition(
    name: str,
    description: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Create tool definition for function calling.

    Args:
        name: Function name
        description: What the function does
        parameters: JSON schema for parameters

    Returns:
        Tool definition dictionary

    Example:
        weather_tool = create_tool_definition(
            name="get_weather",
            description="Get weather in a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. Chicago, IL"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        )
    """
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters
        }
    }
