"""
JWT認証・パスワードハッシュ機能

JWTトークンの生成・検証、パスワードのハッシュ化・検証を提供
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# パスワードハッシュ設定（bcrypt使用）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT設定
# 本番環境では環境変数から取得すること
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 86400  # 24時間


class TokenData(BaseModel):
    """JWTトークンのペイロードデータ"""

    salesperson_id: int | None = None
    email: str | None = None


class Token(BaseModel):
    """トークンレスポンス"""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_SECONDS


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    パスワードを検証する

    Args:
        plain_password: 平文パスワード
        hashed_password: ハッシュ化されたパスワード

    Returns:
        検証結果（True: 一致、False: 不一致）
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化する

    Args:
        password: 平文パスワード

    Returns:
        ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    JWTアクセストークンを生成する

    Args:
        data: トークンに含めるデータ（sub, emailなど）
        expires_delta: 有効期限（デフォルト: 24時間）

    Returns:
        生成されたJWTトークン
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=ACCESS_TOKEN_EXPIRE_SECONDS
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData | None:
    """
    JWTアクセストークンをデコードする

    Args:
        token: JWTトークン

    Returns:
        デコードされたトークンデータ（無効な場合はNone）
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        salesperson_id: int | None = payload.get("sub")
        email: str | None = payload.get("email")
        if salesperson_id is None:
            return None
        return TokenData(salesperson_id=salesperson_id, email=email)
    except JWTError:
        return None
