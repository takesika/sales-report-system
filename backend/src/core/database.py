"""データベース接続モジュール.

SQLAlchemy AsyncSessionの設定とFastAPI依存性注入用の関数を提供する。
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings


class Base(DeclarativeBase):
    """SQLAlchemyモデルの基底クラス.

    全てのORMモデルはこのクラスを継承する。
    """

    pass


# 非同期エンジンの作成
engine = create_async_engine(
    settings.async_database_url,
    echo=settings.debug,  # デバッグモード時はSQLをログ出力
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,  # 接続確認を行う
)

# 非同期セッションファクトリ
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # コミット後もオブジェクトを使用可能に
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI依存性注入用のデータベースセッション取得関数.

    使用例:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()

    Yields:
        AsyncSession: データベースセッション

    Note:
        セッションはリクエスト終了時に自動的にクローズされる。
        例外発生時は自動的にロールバックされる。
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """コンテキストマネージャとしてのデータベースセッション取得.

    FastAPIの依存性注入以外の場所で使用する場合に使う。

    使用例:
        async with get_db_context() as db:
            result = await db.execute(select(Item))
            items = result.scalars().all()

    Yields:
        AsyncSession: データベースセッション
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """データベース初期化.

    テーブルの作成などを行う。開発環境やテスト環境で使用。
    本番環境ではマイグレーションツールを使用すること。
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """データベース接続のクローズ.

    アプリケーション終了時に呼び出す。
    """
    await engine.dispose()
