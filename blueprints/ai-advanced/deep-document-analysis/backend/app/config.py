from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = "Deep Document Analysis API"
    api_version: str = "v1"
    chroma_persist_directory: Path = Path(__file__).resolve().parent.parent / "storage" / "chroma"
    embedding_model: str = Field("sentence-transformers/all-MiniLM-L6-v2", description="Sentence transformer used for embeddings")
    chunk_size: int = 1200
    chunk_overlap: int = 150

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.chroma_persist_directory.mkdir(parents=True, exist_ok=True)
    return settings
