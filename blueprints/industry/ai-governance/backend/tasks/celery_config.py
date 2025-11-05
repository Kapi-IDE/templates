"""
Celery Task Queue Configuration Component

Provides production-ready Celery setup for background task processing.
All secrets managed via environment variables.

Usage:
    from components.backend.task_queue.celery_config import celery_app

    @celery_app.task
    def my_background_task(data):
        # Your task logic here
        pass
"""

from celery import Celery
import os


def create_celery_app(
    app_name: str = "kapi",
    broker_url: str = None,
    backend_url: str = None,
    imports: list = None,
) -> Celery:
    """Create and configure a Celery application.

    Args:
        app_name: Application name for Celery
        broker_url: Message broker URL (defaults to env: CELERY_BROKER_URL)
        backend_url: Result backend URL (defaults to env: CELERY_RESULT_BACKEND)
        imports: List of modules containing tasks to import

    Returns:
        Configured Celery application instance

    Environment Variables:
        CELERY_BROKER_URL: Redis/RabbitMQ broker URL (default: redis://localhost:6379/0)
        CELERY_RESULT_BACKEND: Result storage URL (default: redis://localhost:6379/0)

    Example:
        # Basic usage
        celery_app = create_celery_app(app_name="my_app")

        # Custom configuration
        celery_app = create_celery_app(
            app_name="my_app",
            imports=['app.tasks', 'app.scheduled_tasks']
        )
    """
    # Get broker and backend from environment or parameters
    broker = broker_url or os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    backend = backend_url or os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Initialize celery
    celery = Celery(app_name, broker=broker, backend=backend)

    # Register task modules
    if imports:
        celery.conf.imports = imports

    # Production-ready configuration
    celery.conf.update(
        # Serialization
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        # Timezone
        timezone="UTC",
        enable_utc=True,
        # Task execution
        task_track_started=True,
        task_time_limit=600,  # 10 minutes max per task
        task_soft_time_limit=540,  # 9 minutes soft limit (warning)
        # Worker optimization
        worker_prefetch_multiplier=1,  # Fetch one task at a time for fairness
        worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks (memory leak prevention)
        # Connection handling
        broker_connection_retry_on_startup=True,
        broker_connection_retry=True,
        broker_connection_max_retries=10,
        # Result backend
        result_expires=3600,  # Results expire after 1 hour
        result_backend_transport_options={"master_name": "mymaster"},
    )

    return celery


# Default instance for simple usage
celery_app = create_celery_app()


# Example task definitions
def register_example_tasks():
    """Example task patterns for reference (not auto-registered)."""

    @celery_app.task(bind=True, max_retries=3)
    def retry_task_example(self, data):
        """Task with automatic retry on failure."""
        try:
            # Your task logic here
            pass
        except Exception as exc:
            # Retry with exponential backoff
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

    @celery_app.task
    def simple_task_example(data):
        """Simple task without retry logic."""
        # Your task logic here
        pass

    @celery_app.task(bind=True)
    def progress_task_example(self, total_items):
        """Task that reports progress."""
        for i in range(total_items):
            # Do work
            # Update progress
            self.update_state(
                state="PROGRESS", meta={"current": i, "total": total_items}
            )
        return {"status": "completed", "total": total_items}


if __name__ == "__main__":
    # Start worker if run directly
    # Usage: python celery_config.py worker --loglevel=info
    celery_app.start()
