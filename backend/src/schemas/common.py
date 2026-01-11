"""共通レスポンススキーマ."""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """エラー詳細."""

    code: str
    message: str


class SuccessResponse[T](BaseModel):
    """成功レスポンス."""

    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    """エラーレスポンス."""

    success: bool = False
    error: ErrorDetail


class MessageData(BaseModel):
    """メッセージデータ."""

    message: str
