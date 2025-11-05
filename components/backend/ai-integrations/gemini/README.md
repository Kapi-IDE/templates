# Gemini Integration (Python)

Production-ready client for Google Gemini with an OpenAI-compatible interface.

## Install
```bash
pip install google-generativeai>=0.6.0
```

## Usage
```python
from client import create_gemini_client, ReasoningEffort

client = create_gemini_client()
response = client.chat.completions.create(
    model="gemini-2.5-pro-preview-05-06",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    reasoning_effort=ReasoningEffort.MEDIUM.value,
)
print(response.choices[0].message['content'])
```

Set `GOOGLE_API_KEY` in your environment before importing the client.
