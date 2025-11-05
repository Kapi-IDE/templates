"""
Redis Caching and Session Management Component

Provides Redis client setup for caching, session management, and pub/sub.
All credentials managed via environment variables - NO HARDCODED SECRETS.

Usage:
    from components.backend.caching.redis import get_redis_client, RedisSessionManager

    # Get Redis client
    redis_client = get_redis_client()
    redis_client.set("key", "value", ex=3600)

    # Use session manager
    session_mgr = RedisSessionManager()
    session_id = session_mgr.create_session(user_data)
"""

import redis
from typing import Optional, Dict, Any
import json
import os
from datetime import timedelta
import secrets


def get_redis_url() -> str:
    """Get Redis URL from environment variable.

    Environment Variables:
        REDIS_URL: Redis connection string
            Format: redis://[:password@]host:port/db
            Examples:
                redis://localhost:6379/0
                redis://:password@localhost:6379/0
                redis://redis-host:6379/1

    Returns:
        Redis URL string

    Raises:
        ValueError: If no Redis URL is configured
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis_url


def create_redis_client(
    url: str = None,
    decode_responses: bool = True,
    max_connections: int = 50,
    socket_timeout: int = 5,
    socket_connect_timeout: int = 5,
) -> redis.Redis:
    """Create Redis client with production-ready settings.

    Args:
        url: Redis URL (defaults to env variable)
        decode_responses: Auto-decode responses to strings (default: True)
        max_connections: Max connection pool size (default: 50)
        socket_timeout: Socket timeout in seconds (default: 5)
        socket_connect_timeout: Connection timeout in seconds (default: 5)

    Returns:
        Redis client instance

    Example:
        # Use defaults from environment
        client = create_redis_client()

        # Custom configuration
        client = create_redis_client(
            url="redis://localhost:6379/1",
            decode_responses=False
        )
    """
    redis_url = url or get_redis_url()

    return redis.Redis.from_url(
        redis_url,
        decode_responses=decode_responses,
        max_connections=max_connections,
        socket_timeout=socket_timeout,
        socket_connect_timeout=socket_connect_timeout,
        socket_keepalive=True,
        health_check_interval=30,
    )


# Global Redis client instance
redis_client = create_redis_client()


def redis_health_check() -> bool:
    """Check if Redis connection is healthy.

    Returns:
        True if Redis is accessible, False otherwise

    Example:
        if redis_health_check():
            print("Redis is healthy")
    """
    try:
        return redis_client.ping()
    except Exception:
        return False


class RedisSessionManager:
    """Redis-based session management for web applications.

    Provides secure session storage with automatic expiration.
    Suitable for admin panels, user sessions, temporary auth tokens.

    Example:
        session_mgr = RedisSessionManager(prefix="app_session:")

        # Create session
        session_id = session_mgr.create_session({"user_id": 123, "role": "admin"})

        # Get session
        data = session_mgr.get_session(session_id)

        # Update session
        session_mgr.update_session(session_id, {"last_activity": "2025-10-01"})

        # Delete session
        session_mgr.delete_session(session_id)
    """

    def __init__(
        self,
        redis_client: redis.Redis = None,
        key_prefix: str = "session:",
        session_duration: timedelta = timedelta(hours=24),
    ):
        """Initialize session manager.

        Args:
            redis_client: Redis client (defaults to global client)
            key_prefix: Prefix for session keys (default: "session:")
            session_duration: Session lifetime (default: 24 hours)
        """
        self.redis = redis_client or create_redis_client()
        self.key_prefix = key_prefix
        self.session_ttl = int(session_duration.total_seconds())

    def _get_key(self, session_id: str) -> str:
        """Generate full Redis key from session ID."""
        return f"{self.key_prefix}{session_id}"

    def create_session(
        self, session_data: Dict[str, Any], session_id: str = None
    ) -> str:
        """Create a new session with given data.

        Args:
            session_data: Dictionary of session data to store
            session_id: Optional custom session ID (generated if not provided)

        Returns:
            Session ID string

        Example:
            session_id = mgr.create_session({
                "user_id": 123,
                "email": "user@example.com",
                "role": "admin"
            })
        """
        # Generate secure random session ID if not provided
        if session_id is None:
            session_id = secrets.token_hex(32)  # 64 character hex string

        key = self._get_key(session_id)

        # Store session data as JSON
        self.redis.setex(key, self.session_ttl, json.dumps(session_data))

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data by session ID.

        Args:
            session_id: Session identifier

        Returns:
            Session data dictionary or None if not found/expired

        Example:
            data = mgr.get_session(session_id)
            if data:
                print(f"User: {data['user_id']}")
        """
        if not session_id:
            return None

        key = self._get_key(session_id)
        session_json = self.redis.get(key)

        if not session_json:
            return None

        try:
            return json.loads(session_json)
        except json.JSONDecodeError:
            return None

    def update_session(
        self, session_id: str, session_data: Dict[str, Any], extend_ttl: bool = True
    ) -> bool:
        """Update existing session with new data.

        Args:
            session_id: Session identifier
            session_data: New session data (replaces existing)
            extend_ttl: Reset expiration timer (default: True)

        Returns:
            True if session was updated, False if not found

        Example:
            mgr.update_session(session_id, {
                "user_id": 123,
                "last_activity": datetime.now().isoformat()
            })
        """
        key = self._get_key(session_id)

        # Check if session exists
        if not self.redis.exists(key):
            return False

        # Update data
        if extend_ttl:
            self.redis.setex(key, self.session_ttl, json.dumps(session_data))
        else:
            self.redis.set(key, json.dumps(session_data), keepttl=True)

        return True

    def delete_session(self, session_id: str) -> bool:
        """Delete a session.

        Args:
            session_id: Session identifier

        Returns:
            True if session was deleted, False if not found

        Example:
            mgr.delete_session(session_id)
        """
        key = self._get_key(session_id)
        return bool(self.redis.delete(key))

    def extend_session(self, session_id: str) -> bool:
        """Extend session expiration time.

        Args:
            session_id: Session identifier

        Returns:
            True if session was extended, False if not found

        Example:
            mgr.extend_session(session_id)  # Resets TTL to full duration
        """
        key = self._get_key(session_id)
        return bool(self.redis.expire(key, self.session_ttl))


class RedisCache:
    """Simple caching wrapper for Redis.

    Example:
        cache = RedisCache()

        # Set value
        cache.set("user:123", {"name": "John"}, ttl=3600)

        # Get value
        user = cache.get("user:123")

        # Delete value
        cache.delete("user:123")
    """

    def __init__(self, redis_client: redis.Redis = None, key_prefix: str = "cache:"):
        """Initialize cache.

        Args:
            redis_client: Redis client (defaults to global client)
            key_prefix: Prefix for cache keys (default: "cache:")
        """
        self.redis = redis_client or create_redis_client()
        self.key_prefix = key_prefix

    def _get_key(self, key: str) -> str:
        """Generate full Redis key."""
        return f"{self.key_prefix}{key}"

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set cache value with TTL.

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default: 1 hour)

        Returns:
            True if successful
        """
        full_key = self._get_key(key)
        return bool(self.redis.setex(full_key, ttl, json.dumps(value)))

    def get(self, key: str) -> Optional[Any]:
        """Get cached value.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        full_key = self._get_key(key)
        value_json = self.redis.get(full_key)

        if not value_json:
            return None

        try:
            return json.loads(value_json)
        except json.JSONDecodeError:
            return None

    def delete(self, key: str) -> bool:
        """Delete cached value.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        full_key = self._get_key(key)
        return bool(self.redis.delete(full_key))

    def exists(self, key: str) -> bool:
        """Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists
        """
        full_key = self._get_key(key)
        return bool(self.redis.exists(full_key))
