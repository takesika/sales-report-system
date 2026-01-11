"""メインAPIのテスト."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    """ルートエンドポイントのテスト."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "営業日報システム API"}


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """ヘルスチェックエンドポイントのテスト."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
