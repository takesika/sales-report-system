"""認証用Dependency."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from .security import decode_access_token

# OAuth2のトークン取得エンドポイント
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class CurrentUser(BaseModel):
    """現在のログインユーザー情報."""

    salesperson_id: int
    email: str | None = None
    name: str | None = None
    manager_id: int | None = None
    is_active: bool = True


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CurrentUser:
    """現在のログインユーザーを取得する.

    JWTトークンを検証し、ユーザー情報を返す。
    トークンが無効な場合は401エラーを返す。

    Args:
        token: Authorizationヘッダーから取得したJWTトークン

    Returns:
        現在のログインユーザー情報

    Raises:
        HTTPException: トークンが無効な場合（401 Unauthorized）
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "success": False,
            "error": {
                "code": "UNAUTHORIZED",
                "message": "認証に失敗しました",
            },
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_access_token(token)
    if token_data is None or token_data.salesperson_id is None:
        raise credentials_exception

    # TODO: データベースからユーザー情報を取得して、
    # is_active=Falseのユーザーを弾く処理を追加
    # 現時点ではトークンの情報のみを返す
    return CurrentUser(
        salesperson_id=token_data.salesperson_id,
        email=token_data.email,
    )


async def get_current_active_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> CurrentUser:
    """アクティブなログインユーザーを取得する.

    無効化されたユーザーの場合は401エラーを返す。

    Args:
        current_user: 現在のログインユーザー

    Returns:
        アクティブなログインユーザー情報

    Raises:
        HTTPException: ユーザーが無効化されている場合（401 Unauthorized）
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "このアカウントは無効化されています",
                },
            },
        )
    return current_user
