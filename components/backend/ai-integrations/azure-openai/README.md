# Azure OpenAI Integration (Python)

Enterprise-grade wrapper around Azure OpenAI with support for GPT and DeepSeek models.

## Install
```bash
pip install openai azure-identity
```

## Usage
```python
from client import create_client

client = create_client()
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Summarize the meeting"}],
)
print(completion.choices[0].message['content'])
```

Configure the following environment variables:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
