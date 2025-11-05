# Celery Configuration Factory

Minimal Celery setup that reads broker/result URLs from environment variables and applies sensible defaults.

## Install
```bash
pip install celery redis
```

## Usage
```python
from celery_config import create_celery_app

celery_app = create_celery_app(imports=['tasks'])

@celery_app.task(bind=True, max_retries=3)
def send_email(self, payload):
    ...
```

Environment variables:
- `CELERY_BROKER_URL` (default `redis://localhost:6379/0`)
- `CELERY_RESULT_BACKEND`
