from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import initialize_application


@pytest.fixture(name="test_app")
def test_app() -> FastAPI:
    return initialize_application()


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(name="async_client")
async def ac(test_app) -> AsyncGenerator:
    async with AsyncClient(
        app=test_app,
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as c:
        yield c
