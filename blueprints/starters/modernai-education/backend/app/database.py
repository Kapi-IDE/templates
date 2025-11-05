from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text

import os
from dotenv import load_dotenv

Base = declarative_base()
load_dotenv("config/.env")

# Expect DATABASE_URL set via environment or config/.env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable must be set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test database connection
def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1")) 
        print("Database connection successful!")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
    finally:
        db.close()

if os.getenv("RUN_DB_CHECK", "true").lower() == "true":
    test_db_connection()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
