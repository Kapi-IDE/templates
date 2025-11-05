"""
Azure OpenAI Integration Component

Provides production-ready Azure OpenAI client with multi-region support.
Includes DeepSeek, embeddings, and special model handling (o3-mini).
All credentials managed via environment variables - NO HARDCODED SECRETS.

Usage:
    from components.backend.ai_integrations.azure_openai import (
        create_azure_openai_client,
        create_azure_embeddings_client,
        chat_completion
    )

    # Create client
    client = create_azure_openai_client(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )

    # Chat completion
    result = chat_completion(
        client=client,
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
"""

import os
import logging
from typing import Any, Dict, List, Optional

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from langchain_openai import AzureOpenAIEmbeddings

logger = logging.getLogger(__name__)


# ====================================================================
# Environment Variable Helpers
# ====================================================================

def get_azure_config() -> Dict[str, str]:
    """Get Azure OpenAI configuration from environment variables.

    Environment Variables:
        AZURE_OPENAI_ENDPOINT: Azure OpenAI endpoint URL
        AZURE_OPENAI_KEY: Azure OpenAI API key
        AZURE_OPENAI_API_VERSION: API version (default: 2024-02-15-preview)

    Returns:
        Dictionary with endpoint, api_key, api_version

    Raises:
        ValueError: If required environment variables are missing
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure OpenAI configuration incomplete. "
            "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables."
        )

    return {
        "endpoint": endpoint,
        "api_key": api_key,
        "api_version": api_version
    }


def get_azure_deepseek_config() -> Dict[str, str]:
    """Get Azure DeepSeek configuration from environment variables.

    Environment Variables:
        AZURE_DEEPSEEK_ENDPOINT: Azure DeepSeek endpoint URL
        AZURE_DEEPSEEK_KEY: Azure DeepSeek API key

    Returns:
        Dictionary with endpoint and api_key

    Raises:
        ValueError: If required environment variables are missing
    """
    endpoint = os.getenv("AZURE_DEEPSEEK_ENDPOINT")
    api_key = os.getenv("AZURE_DEEPSEEK_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure DeepSeek configuration incomplete. "
            "Set AZURE_DEEPSEEK_ENDPOINT and AZURE_DEEPSEEK_KEY environment variables."
        )

    return {
        "endpoint": endpoint,
        "api_key": api_key
    }


# ====================================================================
# Client Creation Functions
# ====================================================================

def create_azure_openai_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: Optional[str] = None
) -> AzureOpenAI:
    """Create Azure OpenAI client.

    Args:
        endpoint: Azure endpoint URL (defaults to env var)
        api_key: API key (defaults to env var)
        api_version: API version (defaults to env var or 2024-02-15-preview)

    Returns:
        Initialized AzureOpenAI client

    Example:
        # Use environment variables
        client = create_azure_openai_client()

        # Custom configuration
        client = create_azure_openai_client(
            endpoint="https://your-resource.openai.azure.com/",
            api_key="your-key-here",
            api_version="2024-02-15-preview"
        )
    """
    config = get_azure_config()

    endpoint = endpoint or config["endpoint"]
    api_key = api_key or config["api_key"]
    api_version = api_version or config["api_version"]

    logger.info(f"Initializing Azure OpenAI client with endpoint: {endpoint}")

    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )


def create_azure_deepseek_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None
) -> ChatCompletionsClient:
    """Create Azure DeepSeek client.

    Args:
        endpoint: Azure DeepSeek endpoint URL (defaults to env var)
        api_key: API key (defaults to env var)

    Returns:
        Initialized ChatCompletionsClient for DeepSeek

    Example:
        client = create_azure_deepseek_client()
    """
    config = get_azure_deepseek_config()

    endpoint = endpoint or config["endpoint"]
    api_key = api_key or config["api_key"]

    logger.info(f"Initializing Azure DeepSeek client with endpoint: {endpoint}")

    return ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )


def create_azure_embeddings_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: Optional[str] = None
) -> AzureOpenAIEmbeddings:
    """Create Azure OpenAI embeddings client.

    Args:
        endpoint: Azure endpoint URL (defaults to env var)
        api_key: API key (defaults to env var)
        api_version: API version (defaults to env var)

    Returns:
        Initialized AzureOpenAIEmbeddings client

    Example:
        embeddings = create_azure_embeddings_client()
        vectors = embeddings.embed_query("Your text here")
    """
    config = get_azure_config()

    endpoint = endpoint or config["endpoint"]
    api_key = api_key or config["api_key"]
    api_version = api_version or config["api_version"]

    logger.info(f"Initializing Azure OpenAI embeddings client with endpoint: {endpoint}")

    return AzureOpenAIEmbeddings(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )


# ====================================================================
# Chat Completion Functions
# ====================================================================

def chat_completion(
    client: AzureOpenAI,
    model: str,
    messages: List[Dict[str, str]],
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    is_o3_mini: bool = False
) -> Dict[str, Any]:
    """Invoke Azure OpenAI chat completion.

    Args:
        client: Initialized Azure OpenAI client
        model: Model deployment name (e.g., "gpt-4", "gpt-35-turbo")
        messages: List of message dicts [{"role": "user", "content": "..."}]
        max_tokens: Maximum completion tokens
        temperature: Sampling temperature 0.0-1.0
        is_o3_mini: Whether model is o3-mini (special parameter handling)

    Returns:
        Dictionary with:
            - content: Response text
            - prompt_tokens: Input token count
            - completion_tokens: Output token count
            - total_tokens: Total token count
            - estimated_cost: Cost estimate (if available)

    Raises:
        Exception: If API call fails

    Example:
        # Standard model
        result = chat_completion(
            client=client,
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=500,
            temperature=0.7
        )
        print(result["content"])

        # o3-mini model (special handling)
        result = chat_completion(
            client=client,
            model="o3-mini",
            messages=[{"role": "user", "content": "Solve this..."}],
            max_tokens=1000,
            is_o3_mini=True  # Omits temperature parameter
        )
    """
    logger.info(f"Invoking Azure OpenAI model: '{model}'")

    try:
        # o3-mini requires max_completion_tokens and doesn't support temperature
        if is_o3_mini:
            response = client.chat.completions.create(
                messages=messages,
                max_completion_tokens=max_tokens,
                model=model
            )
        else:
            response = client.chat.completions.create(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                model=model
            )

        result = {
            "content": response.choices[0].message.content,
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
            "estimated_cost": None
        }

        # Extract usage statistics if available
        if hasattr(response, "usage"):
            result["prompt_tokens"] = getattr(response.usage, "prompt_tokens", None)
            result["completion_tokens"] = getattr(response.usage, "completion_tokens", None)
            result["total_tokens"] = getattr(response.usage, "total_tokens", None)

        return result

    except Exception as e:
        logger.error(f"Error invoking Azure OpenAI model '{model}': {e}")
        raise


def deepseek_completion(
    client: ChatCompletionsClient,
    model: str,
    messages: List[Dict[str, str]],
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None
) -> Dict[str, Any]:
    """Invoke Azure DeepSeek chat completion.

    Args:
        client: Initialized Azure DeepSeek client
        model: Model deployment name
        messages: List of message dicts [{"role": "user", "content": "..."}]
        max_tokens: Maximum completion tokens
        temperature: Sampling temperature 0.0-1.0

    Returns:
        Dictionary with content and usage statistics

    Raises:
        Exception: If API call fails
        ValueError: If message structure is invalid

    Example:
        result = deepseek_completion(
            client=client,
            model="deepseek-coder",
            messages=[
                {"role": "system", "content": "You are a coding assistant"},
                {"role": "user", "content": "Write a function to reverse a string"}
            ],
            max_tokens=500
        )
    """
    logger.info(f"Invoking Azure DeepSeek model: '{model}'")

    try:
        # Adapt messages for DeepSeek's expected format
        azure_messages = []
        if messages and messages[0].get("role") == "system":
            azure_messages.append(SystemMessage(content=messages[0]["content"]))
            if len(messages) > 1 and messages[1].get("role") == "user":
                azure_messages.append(UserMessage(content=messages[1]["content"]))
        elif messages and messages[0].get("role") == "user":
            azure_messages.append(UserMessage(content=messages[0]["content"]))

        if not azure_messages:
            raise ValueError("Invalid message structure for DeepSeek")

        response = client.complete(
            messages=azure_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            model=model
        )

        result = {
            "content": response.choices[0].message.content,
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
            "estimated_cost": None
        }

        # Extract usage statistics if available
        if hasattr(response, "usage"):
            result["prompt_tokens"] = getattr(response.usage, "prompt_tokens", None)
            result["completion_tokens"] = getattr(response.usage, "completion_tokens", None)
            result["total_tokens"] = getattr(response.usage, "total_tokens", None)

        return result

    except Exception as e:
        logger.error(f"Error invoking Azure DeepSeek model '{model}': {e}")
        raise


# ====================================================================
# Health Check
# ====================================================================

def azure_openai_health_check(client: Optional[AzureOpenAI] = None) -> bool:
    """Check if Azure OpenAI client is functioning properly.

    Args:
        client: Optional client to test (creates new one if not provided)

    Returns:
        True if healthy, False otherwise

    Example:
        if azure_openai_health_check():
            print("Azure OpenAI is ready")
    """
    try:
        if client is None:
            client = create_azure_openai_client()

        result = chat_completion(
            client=client,
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo"),
            messages=[{"role": "user", "content": "Say 'OK'"}],
            max_tokens=10
        )
        return bool(result.get("content"))
    except Exception:
        return False
