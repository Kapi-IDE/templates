import os
from client import create_redis_client, RedisSessionManager, DistributedLock


def test_client_and_session_manager_instantiates_without_connection():
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
    client = create_redis_client()
    assert client is not None

    session_manager = RedisSessionManager(client=client)
    session_id = session_manager.create_session({"user_id": 1})
    assert isinstance(session_id, str)

    # Lock context should not raise when Redis is unreachable (lazy connection)
    lock = DistributedLock(client, "resource")
    assert lock.name == "resource"
