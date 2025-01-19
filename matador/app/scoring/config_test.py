# matador/tests/conftest.py
import pytest
from httpx import AsyncClient
import asyncio
import sys
from pathlib import Path
import os

# Add the project root directory to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from ..main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_client():
    """Create an async client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client