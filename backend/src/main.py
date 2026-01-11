"""営業日報システム FastAPI エントリーポイント."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import auth

app = FastAPI(
    title="営業日報システム API",
    description="営業担当者が日々の顧客訪問活動を報告するシステム",
    version="0.1.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """ヘルスチェック用エンドポイント."""
    return {"message": "営業日報システム API"}


@app.get("/api/v1/health")
async def health_check() -> dict[str, str]:
    """APIヘルスチェック."""
    return {"status": "ok"}


# APIルーターを登録
app.include_router(auth.router, prefix="/api/v1")
