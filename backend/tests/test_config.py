"""設定モジュールのテスト."""

import os
from unittest.mock import patch


class TestSettings:
    """Settingsクラスのテスト."""

    def test_default_values(self) -> None:
        """デフォルト値が正しく設定されること."""
        # キャッシュをクリアして新しいインスタンスを作成
        from src.core.config import Settings

        settings = Settings()

        assert settings.db_host == "localhost"
        assert settings.db_port == 3306
        assert settings.db_name == "sales_report_system"
        assert settings.db_pool_size == 5
        assert settings.jwt_algorithm == "HS256"
        assert settings.jwt_expire_seconds == 86400

    def test_async_database_url_from_individual_vars(self) -> None:
        """個別変数から非同期URLが構築されること."""
        from src.core.config import Settings

        settings = Settings(
            db_host="testhost",
            db_port=3307,
            db_user="testuser",
            db_password="testpass",
            db_name="testdb",
        )

        expected = "mysql+aiomysql://testuser:testpass@testhost:3307/testdb"
        assert settings.async_database_url == expected

    def test_async_database_url_from_database_url(self) -> None:
        """DATABASE_URLから非同期URLが変換されること."""
        from src.core.config import Settings

        # mysql:// 形式
        settings = Settings(database_url="mysql://user:pass@host:3306/db")
        assert settings.async_database_url == "mysql+aiomysql://user:pass@host:3306/db"

        # mysql+pymysql:// 形式
        settings = Settings(database_url="mysql+pymysql://user:pass@host:3306/db")
        assert settings.async_database_url == "mysql+aiomysql://user:pass@host:3306/db"

        # mysql+aiomysql:// 形式（そのまま）
        settings = Settings(database_url="mysql+aiomysql://user:pass@host:3306/db")
        assert settings.async_database_url == "mysql+aiomysql://user:pass@host:3306/db"

    def test_sync_database_url_from_individual_vars(self) -> None:
        """個別変数から同期URLが構築されること."""
        from src.core.config import Settings

        settings = Settings(
            db_host="testhost",
            db_port=3307,
            db_user="testuser",
            db_password="testpass",
            db_name="testdb",
        )

        expected = "mysql+pymysql://testuser:testpass@testhost:3307/testdb"
        assert settings.sync_database_url == expected

    def test_sync_database_url_from_database_url(self) -> None:
        """DATABASE_URLから同期URLが変換されること."""
        from src.core.config import Settings

        # mysql:// 形式
        settings = Settings(database_url="mysql://user:pass@host:3306/db")
        assert settings.sync_database_url == "mysql+pymysql://user:pass@host:3306/db"

        # mysql+aiomysql:// 形式
        settings = Settings(database_url="mysql+aiomysql://user:pass@host:3306/db")
        assert settings.sync_database_url == "mysql+pymysql://user:pass@host:3306/db"

    def test_env_var_override(self) -> None:
        """環境変数で設定が上書きされること."""
        from src.core.config import Settings

        with patch.dict(
            os.environ,
            {
                "DB_HOST": "envhost",
                "DB_PORT": "3308",
                "DEBUG": "true",
            },
        ):
            settings = Settings()
            assert settings.db_host == "envhost"
            assert settings.db_port == 3308
            assert settings.debug is True


class TestGetSettings:
    """get_settings関数のテスト."""

    def test_returns_settings_instance(self) -> None:
        """Settings インスタンスが返されること."""
        from src.core.config import get_settings

        # キャッシュをクリア
        get_settings.cache_clear()

        settings = get_settings()
        assert settings is not None
        assert hasattr(settings, "db_host")
        assert hasattr(settings, "async_database_url")

    def test_cached_instance(self) -> None:
        """同じインスタンスがキャッシュされること."""
        from src.core.config import get_settings

        get_settings.cache_clear()

        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
