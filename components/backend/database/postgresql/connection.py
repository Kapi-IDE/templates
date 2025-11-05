"""
PostgreSQL Database Connection Component

Provides SQLAlchemy database setup with session management and dependency injection.
All credentials managed via environment variables - NO HARDCODED SECRETS.

Usage:
    from components.backend.database.postgresql import get_db, Base, engine

    # Use in FastAPI dependency injection
    @app.get("/users")
    def get_users(db: Session = Depends(get_db)):
        return db.query(User).all()
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os


def get_database_url() -> str:
    """Get database URL from environment variable.

    Environment Variables:
        DATABASE_URL or DB_URL: PostgreSQL connection string
            Format: postgresql://username:password@host:port/database
            Example: postgresql://user:pass@localhost:5432/mydb

    Returns:
        Database URL string

    Raises:
        ValueError: If no database URL is configured
    """
    db_url = os.getenv("DATABASE_URL") or os.getenv("DB_URL")

    if not db_url:
        raise ValueError(
            "Database URL not configured. "
            "Set DATABASE_URL or DB_URL environment variable. "
            "Format: postgresql://username:password@host:port/database"
        )

    return db_url


def create_database_engine(
    database_url: str = None,
    echo: bool = False,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_pre_ping: bool = True,
):
    """Create SQLAlchemy engine with production-ready settings.

    Args:
        database_url: Database URL (defaults to env variable)
        echo: Enable SQL query logging (default: False)
        pool_size: Connection pool size (default: 5)
        max_overflow: Max overflow connections (default: 10)
        pool_pre_ping: Test connections before use (default: True)

    Returns:
        SQLAlchemy Engine instance

    Example:
        # Use defaults from environment
        engine = create_database_engine()

        # Custom configuration
        engine = create_database_engine(
            echo=True,  # Enable SQL logging
            pool_size=10,
            max_overflow=20
        )
    """
    url = database_url or get_database_url()

    return create_engine(
        url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=pool_pre_ping,  # Verify connections before use
        pool_recycle=3600,  # Recycle connections after 1 hour
    )


# Create global engine instance
engine = create_database_engine()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Database session dependency for FastAPI.

    Yields a database session and ensures it's closed after use.
    Use with FastAPI's Depends() for automatic session management.

    Yields:
        SQLAlchemy Session

    Example:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    """Create all database tables defined in models.

    Call this after importing all models to create tables.

    Example:
        from app.models import User, Product  # Import all models first
        from components.backend.database.postgresql import create_all_tables

        create_all_tables()  # Creates all tables
    """
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Drop all database tables.

    WARNING: This will delete ALL data. Use only in development/testing.

    Example:
        from components.backend.database.postgresql import drop_all_tables

        drop_all_tables()  # Deletes all tables and data
    """
    Base.metadata.drop_all(bind=engine)


# Context manager for manual session handling
class DatabaseSession:
    """Context manager for manual database session handling.

    Use when you need a session outside of FastAPI dependency injection.

    Example:
        from components.backend.database.postgresql import DatabaseSession

        with DatabaseSession() as db:
            user = db.query(User).first()
            print(user.name)
    """

    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
        self.db.close()


# Health check function
def database_health_check() -> bool:
    """Check if database connection is healthy.

    Returns:
        True if database is accessible, False otherwise

    Example:
        from components.backend.database.postgresql import database_health_check

        if database_health_check():
            print("Database is healthy")
        else:
            print("Database connection failed")
    """
    try:
        with DatabaseSession() as db:
            db.execute("SELECT 1")
        return True
    except Exception:
        return False
