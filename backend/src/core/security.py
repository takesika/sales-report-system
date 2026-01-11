"""セキュリティ関連ユーティリティ."""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.core.config import settings

# パスワードハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """JWTトークンのペイロードデータ."""

    salesperson_id: int | None = None
    email: str | None = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証する.

    Args:
        plain_password: 平文パスワード
        hashed_password: ハッシュ化されたパスワード

    Returns:
        パスワードが一致する場合True
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化する.

    Args:
        password: 平文パスワード

    Returns:
        ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """アクセストークンを生成する.

    Args:
        data: トークンに含めるデータ
        expires_delta: 有効期限

    Returns:
        JWTトークン文字列
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(seconds=settings.JWT_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> TokenData | None:
    """JWTアクセストークンをデコードする.

    Args:
        token: JWTトークン

    Returns:
        デコードされたトークンデータ（無効な場合はNone）
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        salesperson_id_str: str | None = payload.get("sub")
        email: str | None = payload.get("email")
        if salesperson_id_str is None:
            return None
        return TokenData(salesperson_id=int(salesperson_id_str), email=email)
    except JWTError:
        return None
