"""
Universal LLM Client (Python/LangChain)

Unified interface for multiple LLM providers compatible with LangChain:
- Groq (Fast & FREE)
- OpenAI (Most reliable)
- Anthropic Claude (Best reasoning)
- Google Gemini (Cheapest cloud)
- Ollama (FREE local)

Usage:
    from universal_llm import create_llm, LLMConfig

    llm = create_llm(LLMConfig(
        provider='groq',
        api_key=os.getenv('GROQ_API_KEY'),
        model='llama-3.3-70b-versatile'
    ))

    response = llm.invoke("Hello, world!")
"""

import os
from typing import Optional, Literal, Dict, Any
from dataclasses import dataclass, field


# Type definitions
LLMProvider = Literal['groq', 'openai', 'anthropic', 'gemini', 'ollama']


@dataclass
class LLMConfig:
    """Configuration for LLM client"""
    provider: LLMProvider
    api_key: Optional[str] = None
    model: Optional[str] = None
    base_url: Optional[str] = None

    # Default parameters
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    streaming: bool = False

    # Provider-specific
    azure_endpoint: Optional[str] = None
    azure_deployment: Optional[str] = None
    azure_api_version: Optional[str] = None
    aws_region: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    # Auto-fill defaults
    def __post_init__(self):
        """Auto-fill defaults based on provider"""
        # Auto-detect API key from environment if not provided
        if not self.api_key:
            self.api_key = self._get_api_key_from_env()

        # Set default models
        if not self.model:
            self.model = self._get_default_model()

    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment based on provider"""
        env_vars = {
            'groq': 'GROQ_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'gemini': 'GOOGLE_API_KEY',
            'ollama': None  # No API key needed
        }
        env_var = env_vars.get(self.provider)
        return os.getenv(env_var) if env_var else None

    def _get_default_model(self) -> str:
        """Get default model based on provider"""
        defaults = {
            'groq': 'llama-3.3-70b-versatile',
            'openai': 'gpt-4o-mini',
            'anthropic': 'claude-3-5-sonnet-20241022',
            'gemini': 'gemini-2.0-flash-exp',
            'ollama': 'llama3.2:latest'
        }
        return defaults.get(self.provider, 'default')


@dataclass
class LLMPricing:
    """Pricing information for LLM providers"""
    provider: str
    model: str
    input_cost_per_1m: float  # $ per 1M input tokens
    output_cost_per_1m: float  # $ per 1M output tokens
    free_tier: Optional[str] = None
    notes: Optional[str] = None


# Pricing database
PRICING_TABLE: Dict[str, LLMPricing] = {
    'groq-llama-3.3-70b-versatile': LLMPricing(
        provider='groq',
        model='llama-3.3-70b-versatile',
        input_cost_per_1m=0.0,
        output_cost_per_1m=0.0,
        free_tier='14,400 requests/day',
        notes='FREE - Fast inference'
    ),
    'openai-gpt-4o-mini': LLMPricing(
        provider='openai',
        model='gpt-4o-mini',
        input_cost_per_1m=0.15,
        output_cost_per_1m=0.60,
        notes='Cheapest OpenAI model'
    ),
    'openai-gpt-4o': LLMPricing(
        provider='openai',
        model='gpt-4o',
        input_cost_per_1m=2.50,
        output_cost_per_1m=10.00,
        notes='Most capable OpenAI model'
    ),
    'anthropic-claude-3-5-sonnet': LLMPricing(
        provider='anthropic',
        model='claude-3-5-sonnet-20241022',
        input_cost_per_1m=3.00,
        output_cost_per_1m=15.00,
        notes='Best reasoning'
    ),
    'gemini-2.0-flash-exp': LLMPricing(
        provider='gemini',
        model='gemini-2.0-flash-exp',
        input_cost_per_1m=0.075,
        output_cost_per_1m=0.30,
        notes='Cheapest cloud LLM (50% cheaper than OpenAI)'
    ),
    'ollama-llama3.2': LLMPricing(
        provider='ollama',
        model='llama3.2:latest',
        input_cost_per_1m=0.0,
        output_cost_per_1m=0.0,
        free_tier='Unlimited (local)',
        notes='FREE - Runs locally'
    ),
}


def create_llm(config: LLMConfig) -> Any:
    """
    Create a LangChain-compatible LLM client

    Args:
        config: LLM configuration

    Returns:
        LangChain LLM instance

    Example:
        >>> from universal_llm import create_llm, LLMConfig
        >>> llm = create_llm(LLMConfig(provider='groq'))
        >>> response = llm.invoke("What is 2+2?")
        >>> print(response.content)
        "4"
    """
    if config.provider == 'groq':
        return _create_groq_llm(config)
    elif config.provider == 'openai':
        return _create_openai_llm(config)
    elif config.provider == 'anthropic':
        return _create_anthropic_llm(config)
    elif config.provider == 'gemini':
        return _create_gemini_llm(config)
    elif config.provider == 'ollama':
        return _create_ollama_llm(config)
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")


def _create_groq_llm(config: LLMConfig):
    """Create Groq LLM instance"""
    try:
        from langchain_groq import ChatGroq
    except ImportError:
        raise ImportError("langchain-groq not installed. Run: pip install langchain-groq")

    return ChatGroq(
        model=config.model,
        api_key=config.api_key,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        streaming=config.streaming
    )


def _create_openai_llm(config: LLMConfig):
    """Create OpenAI LLM instance"""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")

    return ChatOpenAI(
        model=config.model,
        api_key=config.api_key,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        streaming=config.streaming
    )


def _create_anthropic_llm(config: LLMConfig):
    """Create Anthropic Claude LLM instance"""
    try:
        from langchain_anthropic import ChatAnthropic
    except ImportError:
        raise ImportError("langchain-anthropic not installed. Run: pip install langchain-anthropic")

    return ChatAnthropic(
        model=config.model,
        api_key=config.api_key,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        streaming=config.streaming
    )


def _create_gemini_llm(config: LLMConfig):
    """Create Google Gemini LLM instance"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError:
        raise ImportError("langchain-google-genai not installed. Run: pip install langchain-google-genai")

    return ChatGoogleGenerativeAI(
        model=config.model,
        google_api_key=config.api_key,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        streaming=config.streaming
    )


def _create_ollama_llm(config: LLMConfig):
    """Create Ollama LLM instance"""
    try:
        from langchain_community.llms import Ollama
    except ImportError:
        raise ImportError("langchain-community not installed. Run: pip install langchain-community")

    return Ollama(
        model=config.model,
        base_url=config.base_url or "http://localhost:11434",
        temperature=config.temperature
    )


def get_pricing(provider: str, model: str) -> Optional[LLMPricing]:
    """
    Get pricing information for a provider and model

    Args:
        provider: LLM provider name
        model: Model name

    Returns:
        Pricing information or None if not found
    """
    key = f"{provider}-{model}"
    return PRICING_TABLE.get(key)


def estimate_cost(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Estimate cost for a request

    Args:
        provider: LLM provider
        model: Model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Estimated cost in dollars
    """
    pricing = get_pricing(provider, model)
    if not pricing:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * pricing.input_cost_per_1m
    output_cost = (output_tokens / 1_000_000) * pricing.output_cost_per_1m

    return input_cost + output_cost


def list_available_providers() -> list[str]:
    """List all available LLM providers"""
    return ['groq', 'openai', 'anthropic', 'gemini', 'ollama']


def get_recommended_provider() -> tuple[str, str]:
    """
    Get recommended provider for general use

    Returns:
        (provider_name, reason) tuple
    """
    return (
        'groq',
        'Fast and FREE with 14,400 requests/day. Best for development and prototyping.'
    )


def get_provider_info(provider: str) -> Dict[str, Any]:
    """
    Get information about a provider

    Args:
        provider: Provider name

    Returns:
        Dictionary with provider information
    """
    info = {
        'groq': {
            'name': 'Groq',
            'cost': 'FREE',
            'speed': 'Fastest',
            'limit': '14,400 requests/day',
            'recommended_for': 'Development, prototyping, high-throughput applications',
            'default_model': 'llama-3.3-70b-versatile',
            'api_key_env': 'GROQ_API_KEY',
            'signup_url': 'https://console.groq.com/keys'
        },
        'openai': {
            'name': 'OpenAI',
            'cost': '$0.15-$30 per 1M tokens',
            'speed': 'Fast',
            'limit': 'Tier-based (starts at 200 req/day)',
            'recommended_for': 'Production applications, most reliable',
            'default_model': 'gpt-4o-mini',
            'api_key_env': 'OPENAI_API_KEY',
            'signup_url': 'https://platform.openai.com/api-keys'
        },
        'anthropic': {
            'name': 'Anthropic Claude',
            'cost': '$3-$15 per 1M tokens',
            'speed': 'Medium',
            'limit': 'Tier-based',
            'recommended_for': 'Complex reasoning, long-form content',
            'default_model': 'claude-3-5-sonnet-20241022',
            'api_key_env': 'ANTHROPIC_API_KEY',
            'signup_url': 'https://console.anthropic.com/'
        },
        'gemini': {
            'name': 'Google Gemini',
            'cost': '$0.075-$7 per 1M tokens (50% cheaper)',
            'speed': 'Fast',
            'limit': '1,500 requests/day (free)',
            'recommended_for': 'Cost optimization, multimodal tasks',
            'default_model': 'gemini-2.0-flash-exp',
            'api_key_env': 'GOOGLE_API_KEY',
            'signup_url': 'https://ai.google.dev/'
        },
        'ollama': {
            'name': 'Ollama',
            'cost': 'FREE (local)',
            'speed': 'Depends on hardware',
            'limit': 'Unlimited',
            'recommended_for': 'Privacy-sensitive applications, offline use',
            'default_model': 'llama3.2:latest',
            'api_key_env': None,
            'signup_url': 'https://ollama.com/'
        }
    }
    return info.get(provider, {})


# Convenience functions
def create_groq_llm(model: str = 'llama-3.3-70b-versatile', **kwargs) -> Any:
    """Create Groq LLM with defaults"""
    return create_llm(LLMConfig(provider='groq', model=model, **kwargs))


def create_openai_llm(model: str = 'gpt-4o-mini', **kwargs) -> Any:
    """Create OpenAI LLM with defaults"""
    return create_llm(LLMConfig(provider='openai', model=model, **kwargs))


def create_anthropic_llm(model: str = 'claude-3-5-sonnet-20241022', **kwargs) -> Any:
    """Create Anthropic LLM with defaults"""
    return create_llm(LLMConfig(provider='anthropic', model=model, **kwargs))


def create_gemini_llm(model: str = 'gemini-2.0-flash-exp', **kwargs) -> Any:
    """Create Gemini LLM with defaults"""
    return create_llm(LLMConfig(provider='gemini', model=model, **kwargs))


def create_ollama_llm(model: str = 'llama3.2:latest', **kwargs) -> Any:
    """Create Ollama LLM with defaults"""
    return create_llm(LLMConfig(provider='ollama', model=model, **kwargs))
