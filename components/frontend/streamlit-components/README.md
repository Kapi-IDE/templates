# Streamlit Atomic Components

Reusable, modular Streamlit components for building custom UIs quickly.

## Components

### 🗨️ [Chat Interface](./chat-interface/)
Reusable chat UI with message display, streaming, and source citations.

**Features:**
- Message history rendering
- Real-time streaming responses
- Source citation expandables
- Chat input box

**Usage:**
```python
from chat_interface import chat

chat.render_chat_messages(messages)
user_input = chat.chat_input()
response = chat.stream_response(generator)
```

---

### 📄 [File Uploader](./file-uploader/)
Document upload with validation and progress tracking.

**Features:**
- File type validation
- Size limits
- Upload progress indicator
- Uploaded files list

**Usage:**
```python
from file_uploader import uploader

file = uploader.file_uploader(allowed_types=['pdf', 'txt'])
success = uploader.upload_with_progress(file, upload_fn)
uploader.render_uploaded_files_list(files)
```

---

### 🔐 [Auth UI](./auth-ui/)
Authentication forms with session management.

**Features:**
- Login form
- Signup form
- Logout button
- Session state management
- Auth guards

**Usage:**
```python
from auth_ui import auth

auth.login_form(on_login=login_fn)
if auth.require_auth():
    # Protected content
    auth.display_user_info()
    auth.logout_button()
```

---

### 🎨 [Dark Theme](./dark-theme/)
Customizable dark themes for Streamlit.

**Features:**
- Onyx palette (default)
- Nord palette
- Dracula palette
- Custom color palettes
- Full component styling

**Usage:**
```python
from dark_theme import theme

theme.apply_dark_theme('onyx')  # or 'nord', 'dracula'
colors = theme.get_theme_colors('onyx')
```

---

## Quick Start

### Install Components

```bash
# Copy all components
cp -r templates/components/frontend/streamlit-components my-project/components

# Or copy individual components
cp -r templates/components/frontend/streamlit-components/chat-interface my-project/
cp -r templates/components/frontend/streamlit-components/dark-theme my-project/
```

### Basic Usage

```python
import streamlit as st
from components.chat_interface import chat
from components.dark_theme import theme

# Apply theme
theme.apply_dark_theme('onyx')

# Initialize state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Render chat
st.title("💬 My Chat App")
chat.render_chat_messages(st.session_state.messages)

if prompt := chat.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Handle response...
```

---

## Component Composition

Build complex UIs by combining atomic components:

### Example: Authenticated RAG App

```python
from components.chat_interface import chat
from components.file_uploader import uploader
from components.auth_ui import auth
from components.dark_theme import theme

# 1. Apply theme
theme.apply_dark_theme('nord')

# 2. Require authentication
if not auth.require_auth():
    auth.login_form(on_login=login_callback)
    st.stop()

# 3. Sidebar with upload
with st.sidebar:
    auth.display_user_info()
    file = uploader.file_uploader(['pdf', 'txt'])
    if file and st.button("Upload"):
        uploader.upload_with_progress(file, upload_callback)
    auth.logout_button()

# 4. Chat interface
chat.render_chat_messages(st.session_state.messages)
if prompt := chat.chat_input():
    # Handle chat...
```

---

## Integration Examples

See [EXAMPLES.md](./EXAMPLES.md) for detailed integration examples:

1. **Simple Chat App** - Basic chat with dark theme
2. **Authenticated Chat** - Login + chat + file upload
3. **Streaming RAG** - Full RAG with FastAPI backend
4. **Multi-Theme Selector** - User-selectable themes
5. **Custom Components** - Using theme colors
6. **Modular Structure** - Organizing larger apps

---

## Component Metadata

Each component includes:
- `metadata.yaml` - Component specification
- Python module with reusable functions
- Inline documentation and examples
- Type hints for better IDE support

### Metadata Structure

```yaml
component_id: streamlit-chat-interface
name: Streamlit Chat Interface
version: 1.0.0
category: frontend
provides: [chat_message_display, streaming_responses]
compatible_with: [streamlit>=1.28.0]
metrics:
  token_count: ~250
  setup_time_minutes: 1
  complexity: simple
```

---

## Best Practices

### 1. State Management
Always initialize session state:

```python
if 'key' not in st.session_state:
    st.session_state.key = default_value
```

### 2. Error Handling
Wrap component calls:

```python
try:
    chat.render_chat_messages(messages)
except Exception as e:
    st.error(f"Error: {e}")
```

### 3. Callbacks
Define callbacks separately:

```python
def on_login(email, password):
    # Login logic
    return token

auth.login_form(on_login=on_login)
```

### 4. Configuration
Use config dictionaries:

```python
CHAT_CONFIG = {
    'placeholder': 'Type here...',
    'show_cursor': True
}

chat.chat_input(**CHAT_CONFIG)
```

---

## Dependencies

All components require:
- `streamlit>=1.28.0`

Additional dependencies per component:
- None (all use standard library)

---

## Customization

### Modify Themes

Edit `dark_theme/theme.py`:

```python
MY_THEME = {
    "bg_primary": "#custom",
    "accent_blue": "#custom",
    # ... more colors
}
```

### Extend Components

Inherit and extend:

```python
from chat_interface import chat

def custom_chat_input(**kwargs):
    # Custom logic
    return chat.chat_input(**kwargs)
```

---

## Testing

Each component includes a `__main__` block for testing:

```bash
# Test individual component
streamlit run components/chat_interface/chat.py

# Test theme
streamlit run components/dark_theme/theme.py
```

---

## Migration from Complete UI

If using the complete [streamlit-rag-ui](../streamlit-rag-ui/):

```bash
# Complete UI (991 tokens)
cp -r templates/components/frontend/streamlit-rag-ui my-project/ui

# Atomic components (more flexible)
cp -r templates/components/frontend/streamlit-components my-project/components
```

Choose based on needs:
- **Complete UI**: Quick deployment, ready-to-use
- **Atomic Components**: Maximum flexibility, composable

---

## Contributing

To add new components:

1. Create component directory
2. Add Python module with functions
3. Create `metadata.yaml`
4. Add usage examples
5. Update this README

---

## License

MIT

---

## Support

For issues or questions:
- See [EXAMPLES.md](./EXAMPLES.md)
- Check [component metadata](./*/metadata.yaml)
- Review [complete UI example](../streamlit-rag-ui/)
