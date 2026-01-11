"""認証API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.config import settings
from src.core.dependencies import CurrentUser, get_current_user
from src.core.security import create_access_token, verify_password
from src.schemas.auth import LoginData, LoginRequest, LoginUser, LogoutData
from src.schemas.common import ErrorDetail, ErrorResponse, SuccessResponse

router = APIRouter(prefix="/auth", tags=["認証"])

# 仮のユーザーデータ（実際はDBから取得）
# TODO: Issue #6, #7 でDB接続実装後に置き換え
MOCK_USERS = {
    "yamada@example.com": {
        "salesperson_id": 1,
        "name": "山田太郎",
        "email": "yamada@example.com",
        # パスワード: password123
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.DfZyJzJX1X1X1O",
        "manager_id": 10,
        "is_active": True,
    },
    "sato@example.com": {
        "salesperson_id": 10,
        "name": "佐藤課長",
        "email": "sato@example.com",
        # パスワード: password123
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.DfZyJzJX1X1X1O",
        "manager_id": None,
        "is_active": True,
    },
    "inactive@example.com": {
        "salesperson_id": 99,
        "name": "無効ユーザー",
        "email": "inactive@example.com",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.DfZyJzJX1X1X1O",
        "manager_id": 10,
        "is_active": False,
    },
}


def authenticate_user(email: str, password: str) -> dict | None:
    """ユーザー認証を行う.

    Args:
        email: メールアドレス
        password: パスワード

    Returns:
        認証成功時はユーザー情報、失敗時はNone
    """
    user = MOCK_USERS.get(email)
    if not user:
        return None
    if not user["is_active"]:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user


@router.post(
    "/login",
    response_model=SuccessResponse[LoginData],
    responses={
        401: {"model": ErrorResponse, "description": "認証エラー"},
    },
    summary="ログイン",
    description="メールアドレスとパスワードで認証し、アクセストークンを発行する",
)
async def login(request: LoginRequest) -> SuccessResponse[LoginData]:
    """ログイン認証を行い、アクセストークンを発行する.

    Args:
        request: ログインリクエスト

    Returns:
        アクセストークンとユーザー情報

    Raises:
        HTTPException: 認証失敗時
    """
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorDetail(
                code="UNAUTHORIZED",
                message="メールアドレスまたはパスワードが正しくありません",
            ).model_dump(),
        )

    # 上長かどうかを判定（manager_idがNullまたは他のユーザーのmanager_idに設定されている場合）
    is_manager = user["manager_id"] is None or any(
        u["manager_id"] == user["salesperson_id"]
        for u in MOCK_USERS.values()
        if u["salesperson_id"] != user["salesperson_id"]
    )

    # アクセストークンを生成
    access_token = create_access_token(
        data={"sub": str(user["salesperson_id"]), "email": user["email"]}
    )

    login_user = LoginUser(
        salesperson_id=user["salesperson_id"],
        name=user["name"],
        email=user["email"],
        is_manager=is_manager,
    )

    login_data = LoginData(
        access_token=access_token,
        expires_in=settings.JWT_EXPIRE_SECONDS,
        user=login_user,
    )

    return SuccessResponse(data=login_data)


@router.post(
    "/logout",
    response_model=SuccessResponse[LogoutData],
    responses={
        401: {"model": ErrorResponse, "description": "認証エラー"},
    },
    summary="ログアウト",
    description="ログアウト処理を行う（トークンの無効化はクライアント側で実施）",
)
async def logout(
    _current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> SuccessResponse[LogoutData]:
    """ログアウト処理を行う.

    JWTトークンの検証を行い、有効であればログアウト成功を返す。
    実際のトークン無効化はクライアント側でトークンを破棄することで実現する。

    Args:
        _current_user: 現在のログインユーザー（認証検証用）

    Returns:
        ログアウト成功メッセージ
    """
    # 認証トークンの検証は get_current_user で実施済み
    # JWTはステートレスなので、サーバー側でのトークン無効化は行わない
    # クライアント側でトークンを破棄することでログアウトを実現

    return SuccessResponse(data=LogoutData(message="ログアウトしました"))
