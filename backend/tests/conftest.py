"""pytest共通設定・フィクスチャ."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """テスト用HTTPクライアント."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
