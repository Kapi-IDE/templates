"""Reusable Streamlit chat interface component."""

import streamlit as st
from typing import Optional, Dict, Any, Generator

def render_chat_messages(messages: list[Dict[str, Any]]):
    """Render chat message history.

    Args:
        messages: List of message dicts with 'role' and 'content' keys
    """
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source.get('source', 'Unknown')}** (chunk {source.get('chunk_index', 0)})")


def chat_input(
    placeholder: str = "Type your message...",
    key: str = "chat_input"
) -> Optional[str]:
    """Render chat input box.

    Args:
        placeholder: Input placeholder text
        key: Streamlit widget key

    Returns:
        User input text or None
    """
    return st.chat_input(placeholder, key=key)


def stream_response(
    response_generator: Generator[str, None, None],
    show_cursor: bool = True
) -> str:
    """Display streaming response with typing indicator.

    Args:
        response_generator: Generator yielding response chunks
        show_cursor: Whether to show typing cursor (▌)

    Returns:
        Complete response text
    """
    response_placeholder = st.empty()
    full_response = ""

    for chunk in response_generator:
        full_response += chunk
        cursor = "▌" if show_cursor else ""
        response_placeholder.markdown(full_response + cursor)

    response_placeholder.markdown(full_response)
    return full_response


def display_message(
    content: str,
    role: str = "assistant",
    sources: Optional[list[Dict]] = None
):
    """Display a single message.

    Args:
        content: Message content
        role: Message role ('user' or 'assistant')
        sources: Optional source citations
    """
    with st.chat_message(role):
        st.markdown(content)

        if sources:
            with st.expander("📚 Sources"):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"**{i}. {source.get('source', 'Unknown')}** (chunk {source.get('chunk_index', 0)})")


# Example usage
if __name__ == "__main__":
    st.set_page_config(page_title="Chat Component Demo", layout="wide")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("💬 Chat Interface Component")

    # Render messages
    render_chat_messages(st.session_state.messages)

    # Chat input
    if prompt := chat_input():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Echo response (for demo)
        with st.chat_message("assistant"):
            response = f"Echo: {prompt}"
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
