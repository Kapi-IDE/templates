"""Streamlit UI for FastAPI RAG Starter - Onyx-inspired dark theme."""

import streamlit as st
import requests
from typing import Optional
import time

# Page config
st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Onyx-like dark theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --bg-tertiary: #3a3a3a;
        --text-primary: #e5e5e5;
        --text-secondary: #a0a0a0;
        --accent-blue: #3b82f6;
        --accent-green: #10b981;
        --border-color: #404040;
    }

    /* Global background */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0f0f0f;
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary);
    }

    /* Chat messages */
    .stChatMessage {
        background-color: var(--bg-secondary);
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border: 1px solid var(--border-color);
    }

    /* User message */
    [data-testid="stChatMessageContent"] {
        background-color: transparent;
    }

    /* Code blocks */
    .stCodeBlock {
        background-color: #1e1e1e !important;
        border-radius: 6px;
        border: 1px solid var(--border-color);
    }

    /* Input boxes */
    .stTextInput > div > div > input {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
    }

    .stTextArea > div > div > textarea {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--accent-blue);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    .stButton > button:hover {
        background-color: #2563eb;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-secondary);
        border: 1px dashed var(--border-color);
        border-radius: 8px;
        padding: 16px;
    }

    /* Success/error messages */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid var(--accent-green);
        color: var(--accent-green);
    }

    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        color: #ef4444;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        border-radius: 6px;
        border: 1px solid var(--border-color);
    }

    /* Divider */
    hr {
        border-color: var(--border-color);
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--text-primary);
    }

    /* Links */
    a {
        color: var(--accent-blue);
    }

    a:hover {
        color: #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

# Helper functions
def login(email: str, password: str) -> Optional[str]:
    """Login and get access token."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/login/access-token",
            data={"username": email, "password": password}
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return None

def upload_document(file, token: str) -> bool:
    """Upload a document to the RAG system."""
    try:
        files = {"file": (file.name, file, file.type)}
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(
            f"{API_BASE_URL}/rag/upload",
            files=files,
            headers=headers
        )
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return False

def query_rag(question: str, token: str, n_results: int = 3) -> Optional[dict]:
    """Query the RAG system."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"question": question, "n_results": n_results}

        response = requests.post(
            f"{API_BASE_URL}/rag/query",
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return None

def stream_query(question: str, token: str, n_results: int = 3):
    """Stream query response from RAG system."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"question": question, "n_results": n_results}

        with requests.post(
            f"{API_BASE_URL}/rag/query/stream",
            json=data,
            headers=headers,
            stream=True
        ) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    yield chunk
    except Exception as e:
        yield f"Error: {str(e)}"

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 RAG Assistant")
    st.markdown("---")

    # Login section
    if not st.session_state.access_token:
        st.markdown("#### 🔐 Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn"):
            token = login(email, password)
            if token:
                st.session_state.access_token = token
                st.success("✅ Logged in successfully!")
                st.rerun()
    else:
        st.success("✅ Logged in")

        if st.button("Logout", key="logout_btn"):
            st.session_state.access_token = None
            st.session_state.messages = []
            st.session_state.uploaded_docs = []
            st.rerun()

        st.markdown("---")

        # Document upload
        st.markdown("#### 📄 Upload Documents")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt"],
            help="Upload PDF or TXT files for RAG",
            label_visibility="collapsed"
        )

        if uploaded_file:
            if st.button("📤 Upload", key="upload_btn"):
                with st.spinner("Uploading..."):
                    if upload_document(uploaded_file, st.session_state.access_token):
                        st.success(f"✅ Uploaded: {uploaded_file.name}")
                        st.session_state.uploaded_docs.append(uploaded_file.name)

        # Uploaded documents list
        if st.session_state.uploaded_docs:
            st.markdown("---")
            st.markdown("#### 📚 Uploaded Documents")
            for doc in st.session_state.uploaded_docs:
                st.markdown(f"• {doc}")

        # Settings
        st.markdown("---")
        st.markdown("#### ⚙️ Settings")
        n_results = st.slider(
            "Context chunks",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of relevant chunks to retrieve"
        )

        stream_response = st.checkbox(
            "Stream responses",
            value=True,
            help="Stream AI responses in real-time"
        )

        # New chat button
        st.markdown("---")
        if st.button("🆕 New Chat", key="new_chat_btn"):
            st.session_state.messages = []
            st.rerun()

# Main chat interface
if not st.session_state.access_token:
    # Welcome screen
    st.markdown("# 🤖 RAG Assistant")
    st.markdown("### Welcome to your AI-powered document Q&A system")
    st.markdown("---")
    st.markdown("""
    **Get started:**
    1. 🔐 Login using the sidebar
    2. 📄 Upload your documents (PDF or TXT)
    3. 💬 Ask questions about your documents

    **Features:**
    - 🔍 Semantic search across documents
    - 🤖 AI-powered answers with GPT-4
    - 📚 Source citations for every answer
    - ⚡ Real-time streaming responses
    """)
else:
    # Chat interface
    st.markdown("# 💬 Chat with your documents")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source['source']}** (chunk {source['chunk_index']})")

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            if stream_response:
                # Streaming response
                response_placeholder = st.empty()
                full_response = ""

                for chunk in stream_query(prompt, st.session_state.access_token, n_results):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)

                # Add to history (without sources for streaming)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })
            else:
                # Non-streaming response
                with st.spinner("Thinking..."):
                    result = query_rag(prompt, st.session_state.access_token, n_results)

                if result:
                    st.markdown(result["answer"])

                    # Show sources
                    if result.get("sources"):
                        with st.expander("📚 Sources"):
                            for i, source in enumerate(result["sources"], 1):
                                st.markdown(f"**{i}. {source['source']}** (chunk {source['chunk_index']})")

                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result.get("sources", [])
                    })

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666;">Powered by FastAPI RAG Starter</div>',
    unsafe_allow_html=True
)
