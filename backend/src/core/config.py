"""アプリケーション設定."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定クラス."""

    # JWT設定
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_SECONDS: int = 86400  # 24時間

    # データベース設定
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/sales_report"

    class Config:
        """Pydantic設定."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
