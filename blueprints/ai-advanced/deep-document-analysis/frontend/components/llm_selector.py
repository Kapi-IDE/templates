import streamlit as st
from dataclasses import dataclass
from typing import List


@dataclass
class ProviderOption:
    value: str
    label: str
    default_model: str
    cost_hint: str
    notes: str


PROVIDERS: List[ProviderOption] = [
    ProviderOption(
        value="groq",
        label="Groq (Llama 3.3 70B)",
        default_model="llama-3.3-70b-versatile",
        cost_hint="FREE (14,400 req/day)",
        notes="Fast inference, ideal for exploration"
    ),
    ProviderOption(
        value="openai",
        label="OpenAI GPT-4o mini",
        default_model="gpt-4o-mini",
        cost_hint="$0.15 / 1M input tokens",
        notes="Balanced quality and cost"
    ),
    ProviderOption(
        value="anthropic",
        label="Anthropic Claude 3.5 Sonnet",
        default_model="claude-3-5-sonnet-20241022",
        cost_hint="$3 / 1M input tokens",
        notes="Best reasoning performance"
    ),
    ProviderOption(
        value="gemini",
        label="Google Gemini 2.0 Flash",
        default_model="gemini-2.0-flash-exp",
        cost_hint="$0.075 / 1M input tokens",
        notes="Cheapest cloud option"
    ),
    ProviderOption(
        value="ollama",
        label="Ollama Local Llama 3.2",
        default_model="llama3.2:latest",
        cost_hint="FREE (runs locally)",
        notes="Great for air-gapped deployments"
    ),
]


def render_llm_selector() -> ProviderOption:
    st.sidebar.subheader("Choose LLM Provider")
    selected = st.sidebar.selectbox(
        "Provider",
        options=PROVIDERS,
        format_func=lambda option: option.label,
        help="Switch providers to compare latency, accuracy, and cost"
    )
    st.sidebar.caption(f"Cost hint: {selected.cost_hint}\n\n{selected.notes}")
    return selected
