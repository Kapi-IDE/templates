# Streamlit Component Integration Examples

This guide shows how to use atomic Streamlit components to build custom UIs.

---

## Example 1: Simple Chat App

Build a minimal chat interface using atomic components.

```python
import streamlit as st
from chat_interface import chat
from dark_theme import theme

# Apply theme
theme.apply_dark_theme('onyx')

# Initialize messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("💬 Simple Chat")

# Display messages
chat.render_chat_messages(st.session_state.messages)

# Get input
if prompt := chat.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mock response
    with st.chat_message("assistant"):
        response = f"Echo: {prompt}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
```

---

## Example 2: Authenticated Chat with File Upload

Combine auth, chat, and file upload components.

```python
import streamlit as st
from chat_interface import chat
from file_uploader import uploader
from auth_ui import auth
from dark_theme import theme

# Apply theme
theme.apply_dark_theme('nord')

# Login required
if not auth.require_auth():
    with st.sidebar:
        def mock_login(email, password):
            return "token_123" if email == "demo@example.com" else None

        auth.login_form(on_login=mock_login)
    st.stop()

# Main app (authenticated)
st.title("📄 Document Chat")

# Sidebar with upload
with st.sidebar:
    auth.display_user_info()
    auth.logout_button()

    st.markdown("---")
    st.markdown("### Upload Documents")

    uploaded_file = uploader.file_uploader(
        allowed_types=['pdf', 'txt'],
        max_size_mb=10
    )

    if uploaded_file and st.button("Upload"):
        def mock_upload(file):
            return True

        uploader.upload_with_progress(uploaded_file, mock_upload)

# Chat interface
if 'messages' not in st.session_state:
    st.session_state.messages = []

chat.render_chat_messages(st.session_state.messages)

if prompt := chat.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = f"Answer based on uploaded documents: {prompt}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
```

---

## Example 3: Streaming RAG Application

Full RAG app with streaming responses.

```python
import streamlit as st
import requests
from chat_interface import chat
from file_uploader import uploader
from auth_ui import auth
from dark_theme import theme

# Config
API_URL = "http://localhost:8000/api/v1"

# Apply theme
theme.apply_dark_theme('dracula')

# Authentication
if not st.session_state.get('access_token'):
    with st.sidebar:
        def login(email, password):
            response = requests.post(f"{API_URL}/login/access-token",
                                   data={"username": email, "password": password})
            return response.json().get('access_token') if response.ok else None

        auth.login_form(on_login=login)
    st.stop()

# Main app
st.title("🤖 RAG Assistant")

# Sidebar
with st.sidebar:
    auth.display_user_info()
    auth.logout_button()

    st.markdown("---")

    # File upload
    uploaded_file = uploader.file_uploader(allowed_types=['pdf', 'txt'])

    if uploaded_file and st.button("Upload"):
        def upload_to_api(file):
            headers = auth.get_auth_headers()
            files = {'file': (file.name, file, file.type)}
            response = requests.post(f"{API_URL}/rag/upload",
                                    files=files, headers=headers)
            return response.ok

        uploader.upload_with_progress(uploaded_file, upload_to_api)

# Chat
if 'messages' not in st.session_state:
    st.session_state.messages = []

chat.render_chat_messages(st.session_state.messages)

if prompt := chat.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Stream response from API
    with st.chat_message("assistant"):
        def stream_from_api():
            headers = auth.get_auth_headers()
            data = {"question": prompt, "n_results": 3}
            with requests.post(f"{API_URL}/rag/query/stream",
                             json=data, headers=headers, stream=True) as r:
                for chunk in r.iter_content(decode_unicode=True):
                    if chunk:
                        yield chunk

        full_response = chat.stream_response(stream_from_api())

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()
```

---

## Example 4: Multi-Theme Selector

Let users choose their preferred theme.

```python
import streamlit as st
from dark_theme import theme

# Theme selector in sidebar
with st.sidebar:
    selected_theme = st.selectbox(
        "🎨 Choose Theme",
        ["onyx", "nord", "dracula"],
        index=0
    )

    # Store in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = selected_theme

    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

# Apply selected theme
theme.apply_dark_theme(st.session_state.theme)

# Rest of your app
st.title(f"App with {st.session_state.theme.title()} Theme")
st.markdown("Theme changes dynamically!")
```

---

## Example 5: Custom Themed Components

Use theme colors in custom components.

```python
import streamlit as st
from dark_theme import theme

# Apply theme
theme.apply_dark_theme('onyx')

# Get color palette
colors = theme.get_theme_colors('onyx')

# Custom styled component
st.markdown(f"""
<div style="
    background-color: {colors['bg_secondary']};
    border: 1px solid {colors['border_color']};
    border-radius: 8px;
    padding: 20px;
    color: {colors['text_primary']};
">
    <h3 style="color: {colors['accent_blue']};">Custom Card</h3>
    <p>This card uses theme colors dynamically!</p>
    <button style="
        background-color: {colors['accent_green']};
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
    ">Action Button</button>
</div>
""", unsafe_allow_html=True)
```

---

## Example 6: Modular App Structure

Organize components into modules for larger apps.

```python
# app.py
import streamlit as st
from components import sidebar, chat_area, theme_config

# Apply theme
theme_config.setup()

# Layout
with st.sidebar:
    sidebar.render()

# Main content
chat_area.render()
```

```python
# components/theme_config.py
import streamlit as st
from dark_theme import theme

def setup():
    theme.apply_dark_theme(
        st.session_state.get('theme', 'onyx')
    )
```

```python
# components/sidebar.py
import streamlit as st
from auth_ui import auth
from file_uploader import uploader

def render():
    if not auth.require_auth():
        auth.login_form(on_login=login_callback)
    else:
        auth.display_user_info()
        st.markdown("---")
        render_upload_section()
        st.markdown("---")
        auth.logout_button()

def render_upload_section():
    file = uploader.file_uploader()
    if file and st.button("Upload"):
        uploader.upload_with_progress(file, upload_callback)
```

```python
# components/chat_area.py
import streamlit as st
from chat_interface import chat

def render():
    st.title("💬 Chat")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    chat.render_chat_messages(st.session_state.messages)

    if prompt := chat.chat_input():
        handle_message(prompt)

def handle_message(prompt):
    # Your chat logic here
    pass
```

---

## Component Composition Best Practices

### 1. State Management
```python
# Initialize all state in one place
def init_session_state():
    defaults = {
        'messages': [],
        'uploaded_files': [],
        'theme': 'onyx',
        'access_token': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()
```

### 2. Callback Functions
```python
# Define callbacks separately
def on_login(email: str, password: str) -> Optional[str]:
    # Login logic
    return token

def on_upload(file) -> bool:
    # Upload logic
    return success

def on_message(prompt: str) -> str:
    # Message handling
    return response

# Use in components
auth.login_form(on_login=on_login)
uploader.upload_with_progress(file, on_upload)
```

### 3. Error Handling
```python
# Wrap component calls in try-except
try:
    chat.render_chat_messages(st.session_state.messages)
except Exception as e:
    st.error(f"Error rendering chat: {str(e)}")
    st.session_state.messages = []  # Reset on error
```

### 4. Configuration
```python
# config.py
CHAT_CONFIG = {
    'placeholder': 'Ask me anything...',
    'show_cursor': True
}

UPLOAD_CONFIG = {
    'allowed_types': ['pdf', 'txt', 'docx'],
    'max_size_mb': 50
}

THEME_CONFIG = {
    'default': 'onyx',
    'options': ['onyx', 'nord', 'dracula']
}

# Use in components
chat.chat_input(**CHAT_CONFIG)
uploader.file_uploader(**UPLOAD_CONFIG)
```

---

## Quick Start Templates

### Minimal Chat
```bash
# Copy only chat component
cp -r components/frontend/streamlit-components/chat-interface .
cp -r components/frontend/streamlit-components/dark-theme .
```

### Auth + Chat
```bash
# Copy auth and chat
cp -r components/frontend/streamlit-components/{chat-interface,auth-ui,dark-theme} .
```

### Full RAG App
```bash
# Copy all components
cp -r components/frontend/streamlit-components/* .
# Or use complete UI
cp -r components/frontend/streamlit-rag-ui .
```

---

## Integration with Backends

### FastAPI
```python
# Use with FastAPI backend
API_URL = "http://localhost:8000/api/v1"
headers = auth.get_auth_headers()
response = requests.post(f"{API_URL}/endpoint", headers=headers, json=data)
```

### Flask
```python
# Use with Flask backend
API_URL = "http://localhost:5000/api"
headers = auth.get_auth_headers()
response = requests.post(f"{API_URL}/endpoint", headers=headers, json=data)
```

### Django
```python
# Use with Django backend
API_URL = "http://localhost:8000/api"
headers = auth.get_auth_headers()
headers['X-CSRFToken'] = get_csrf_token()  # If CSRF enabled
response = requests.post(f"{API_URL}/endpoint", headers=headers, json=data)
```

---

## Troubleshooting

### Component Not Found
```python
# Ensure components are in Python path
import sys
sys.path.insert(0, './components')

# Or use relative imports
from .chat_interface import chat
```

### Theme Not Applied
```python
# Apply theme AFTER st.set_page_config
st.set_page_config(page_title="App", layout="wide")
theme.apply_dark_theme('onyx')  # After config
```

### State Issues
```python
# Always check state before using
if 'messages' in st.session_state:
    chat.render_chat_messages(st.session_state.messages)
else:
    st.warning("No messages yet")
```

---

For more examples, see the complete [streamlit-rag-ui](../streamlit-rag-ui/) implementation.
