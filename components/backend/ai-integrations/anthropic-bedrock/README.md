# Anthropic Claude (AWS Bedrock)

Simplified client for invoking Claude via AWS Bedrock with retries and model mapping.

## Install
```bash
pip install boto3
```

## Usage
```python
from client import create_client

client = create_client()
response = client.generate(
    model="claude-3-5-sonnet",
    messages=[{"role": "user", "content": "Draft a legal summary"}],
)
print(response['content'][0]['text'])
```

Set AWS credentials using the standard environment variables or profile configuration.
