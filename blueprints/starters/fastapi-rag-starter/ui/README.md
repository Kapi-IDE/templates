# RAG Assistant UI

Streamlit-based UI for FastAPI RAG Starter with Onyx-inspired dark theme.

## Features

- 🎨 **Dark Theme** - Onyx-inspired UI with custom CSS
- 💬 **Chat Interface** - Clean conversation flow
- 📄 **Document Upload** - Drag-and-drop PDF/TXT files
- ⚡ **Streaming Responses** - Real-time AI answers
- 📚 **Source Citations** - Track answer sources
- 🔐 **Authentication** - Secure login via FastAPI backend

## Quick Start

### 1. Install Dependencies

```bash
cd ui
pip install -r requirements.txt
```

### 2. Start FastAPI Backend

Make sure the backend is running on `http://localhost:8000`:

```bash
cd ..
fastapi dev app/main.py
```

### 3. Run Streamlit UI

```bash
streamlit run app.py
```

The UI will open at `http://localhost:8501`

## Usage

1. **Login** - Use your FastAPI credentials in the sidebar
2. **Upload Documents** - Click file uploader and select PDF/TXT files
3. **Ask Questions** - Type in the chat input to query your documents
4. **View Sources** - Expand source citations to see references

## Configuration

### API Base URL

Default: `http://localhost:8000/api/v1`

To change, edit `app.py`:

```python
API_BASE_URL = "http://your-api-url:8000/api/v1"
```

### Settings

Adjust in the sidebar:
- **Context chunks** - Number of relevant chunks to retrieve (1-10)
- **Stream responses** - Toggle real-time streaming

## Theme Customization

The UI uses CSS variables for easy theming. Edit colors in `app.py`:

```css
:root {
    --bg-primary: #1a1a1a;      /* Main background */
    --bg-secondary: #2d2d2d;    /* Cards, inputs */
    --bg-tertiary: #3a3a3a;     /* Hover states */
    --text-primary: #e5e5e5;    /* Main text */
    --text-secondary: #a0a0a0;  /* Secondary text */
    --accent-blue: #3b82f6;     /* Primary accent */
    --accent-green: #10b981;    /* Success states */
    --border-color: #404040;    /* Borders */
}
```

## Features in Detail

### Document Upload
- Supports PDF and TXT files
- Real-time upload progress
- Document list in sidebar
- Automatic chunking and indexing

### Chat Interface
- Persistent chat history
- User/assistant message styling
- Code block syntax highlighting
- Source citation expandables

### Streaming
- Real-time response generation
- Typing indicator (▌)
- Smooth text rendering
- Fallback to non-streaming mode

## Troubleshooting

### "Connection refused" error
- Ensure FastAPI backend is running on port 8000
- Check `API_BASE_URL` in `app.py`

### "Login failed" error
- Verify credentials match FastAPI user
- Check `FIRST_SUPERUSER` in backend `.env`

### Documents not uploading
- Check file size (<10MB recommended)
- Verify file type is PDF or TXT
- Ensure you're logged in

### Styling issues
- Clear browser cache
- Refresh page (Ctrl/Cmd + R)
- Check browser console for errors

## Development

### Run in Development Mode

```bash
streamlit run app.py --server.runOnSave true
```

This enables auto-reload on file changes.

### Debug Mode

Enable Streamlit debugging:

```bash
streamlit run app.py --logger.level debug
```

## Docker Deployment

### Build Image

```bash
docker build -t rag-ui .
```

### Run Container

```bash
docker run -p 8501:8501 \
  -e API_BASE_URL=http://backend:8000/api/v1 \
  rag-ui
```

### Docker Compose

Add to `docker-compose.yml`:

```yaml
ui:
  build: ./ui
  ports:
    - "8501:8501"
  environment:
    - API_BASE_URL=http://backend:8000/api/v1
  depends_on:
    - backend
```

## Screenshots

### Main Interface
- Dark theme with Onyx-inspired design
- Sidebar navigation
- Chat messages with code highlighting
- Document upload area

### Features
- Real-time streaming responses
- Source citations with expandables
- Responsive layout
- Clean, modern UI

## Tech Stack

- **Streamlit** - Web framework
- **Requests** - HTTP client
- **Custom CSS** - Dark theme styling

## License

MIT
