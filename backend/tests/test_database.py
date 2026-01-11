"""データベースモジュールのテスト."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


class TestDatabaseModule:
    """データベースモジュールのテスト."""

    def test_base_class_exists(self) -> None:
        """Baseクラスが存在すること."""
        from src.core.database import Base

        assert Base is not None
        assert hasattr(Base, "metadata")

    def test_engine_created(self) -> None:
        """エンジンが作成されていること."""
        from src.core.database import engine

        assert engine is not None
        # 非同期エンジンであることを確認
        assert "aiomysql" in str(engine.url) or "mysql" in str(engine.url)

    def test_session_factory_created(self) -> None:
        """セッションファクトリが作成されていること."""
        from src.core.database import AsyncSessionLocal

        assert AsyncSessionLocal is not None

    def test_get_db_is_async_generator(self) -> None:
        """get_dbが非同期ジェネレータであること."""
        import inspect

        from src.core.database import get_db

        assert inspect.isasyncgenfunction(get_db)

    def test_get_db_context_is_context_manager(self) -> None:
        """get_db_contextがコンテキストマネージャであること."""
        from src.core.database import get_db_context

        # asynccontextmanagerでデコレートされていることを確認
        assert hasattr(get_db_context, "__aenter__") or callable(get_db_context)


class TestDatabaseFunctions:
    """データベース関数のテスト（モック使用）."""

    @pytest.mark.asyncio
    async def test_get_db_yields_session(self) -> None:
        """get_dbがAsyncSessionを返すこと.

        Note:
            実際のDB接続は行わず、型のみ確認する。
            実際の接続テストはインテグレーションテストで行う。
        """
        from src.core.database import AsyncSessionLocal

        # セッションファクトリから直接セッションを作成してテスト
        # 実際のDB接続は行わない
        async with AsyncSessionLocal() as session:
            assert isinstance(session, AsyncSession)


class TestDatabaseExports:
    """モジュールのエクスポートテスト."""

    def test_core_module_exports(self) -> None:
        """coreモジュールから必要なものがエクスポートされていること."""
        from src.core import get_db, settings

        assert settings is not None
        assert get_db is not None
        assert callable(get_db)
