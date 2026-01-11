"""認証関連スキーマ."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """ログインリクエスト."""

    email: EmailStr
    password: str


class LoginUser(BaseModel):
    """ログインユーザー情報."""

    salesperson_id: int
    name: str
    email: str
    is_manager: bool


class LoginData(BaseModel):
    """ログイン成功時のデータ."""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: LoginUser


class LogoutData(BaseModel):
    """ログアウト成功時のデータ."""

    message: str
