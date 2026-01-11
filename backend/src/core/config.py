"""アプリケーション設定モジュール.

環境変数から設定を読み込み、Pydantic Settingsで管理する。
"""

from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定.

    環境変数または.envファイルから設定を読み込む。
    DATABASE_URLが設定されている場合はそれを優先し、
    個別のDB_*変数が設定されている場合はそれらから接続URLを構築する。
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # アプリケーション設定
    app_name: str = Field(default="営業日報システム API")
    debug: bool = Field(default=False)

    # データベース設定（個別指定）
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=3306)
    db_user: str = Field(default="root")
    db_password: str = Field(default="")
    db_name: str = Field(default="sales_report_system")

    # データベース接続URL（直接指定、優先される）
    database_url: str | None = Field(default=None)

    # コネクションプール設定
    db_pool_size: int = Field(default=5)
    db_max_overflow: int = Field(default=10)
    db_pool_timeout: int = Field(default=30)
    db_pool_recycle: int = Field(default=1800)  # 30分

    # JWT設定
    jwt_secret_key: str = Field(default="your-secret-key-change-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_seconds: int = Field(default=86400)  # 24時間

    # CORS設定
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_database_url(self) -> str:
        """非同期用データベースURL.

        DATABASE_URLが設定されている場合はそれを非同期ドライバ用に変換し、
        設定されていない場合は個別のDB_*変数から構築する。
        """
        if self.database_url:
            # mysql:// または mysql+pymysql:// を mysql+aiomysql:// に変換
            url = self.database_url
            if url.startswith("mysql://"):
                return url.replace("mysql://", "mysql+aiomysql://", 1)
            if url.startswith("mysql+pymysql://"):
                return url.replace("mysql+pymysql://", "mysql+aiomysql://", 1)
            if url.startswith("mysql+aiomysql://"):
                return url
            # その他の形式はそのまま返す
            return url

        # 個別変数から構築
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sync_database_url(self) -> str:
        """同期用データベースURL（マイグレーション等で使用）."""
        if self.database_url:
            url = self.database_url
            if url.startswith("mysql://"):
                return url.replace("mysql://", "mysql+pymysql://", 1)
            if url.startswith("mysql+aiomysql://"):
                return url.replace("mysql+aiomysql://", "mysql+pymysql://", 1)
            if url.startswith("mysql+pymysql://"):
                return url
            return url

        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    """設定のシングルトンインスタンスを取得.

    lru_cacheにより、一度読み込んだ設定はキャッシュされる。
    """
    return Settings()


# グローバル設定インスタンス
settings = get_settings()
