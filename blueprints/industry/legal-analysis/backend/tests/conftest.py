"""Shared pytest fixtures for the legal analysis backend."""

import os
import pytest

# Enable lightweight stub mode before importing the Flask app
os.environ.setdefault("LEGAL_BLUEPRINT_UNIT_TEST", "true")

from app import app  # noqa: E402  - import after env configuration


@pytest.fixture()
def client():
    with app.test_client() as test_client:
        yield test_client
