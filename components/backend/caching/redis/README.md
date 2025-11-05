# Redis Client & Session Manager (Python)

Utility helpers for connecting to Redis, managing encrypted sessions, and implementing distributed locks.

## Install
```bash
pip install redis cryptography
```

## Usage
```python
from client import get_redis_client, RedisSessionManager, DistributedLock

redis_client = get_redis_client()
redis_client.set("foo", "bar", ex=3600)

session_mgr = RedisSessionManager()
session_id = session_mgr.create_session({"user_id": 123})

with DistributedLock(redis_client, "resource-key"):
    # critical section
    pass
```

Environment variables:
- `REDIS_URL` – connection string (default `redis://localhost:6379/0`)
