"""営業担当者モデル定義。"""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .daily_report import DailyReport
    from .report_comment import ReportComment


class Salesperson(Base, TimestampMixin):
    """営業担当者モデル。

    上長も同一テーブルで管理し、manager_idで階層構造を表現する。
    """

    __tablename__ = "SALESPERSON"

    salesperson_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    manager_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("SALESPERSON.salesperson_id"),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # 自己参照リレーション
    manager: Mapped["Salesperson | None"] = relationship(
        "Salesperson",
        remote_side=[salesperson_id],
        back_populates="subordinates",
    )
    subordinates: Mapped[list["Salesperson"]] = relationship(
        "Salesperson",
        back_populates="manager",
    )

    # 日報とのリレーション
    daily_reports: Mapped[list["DailyReport"]] = relationship(
        "DailyReport",
        back_populates="salesperson",
    )

    # コメントとのリレーション（この担当者が投稿したコメント）
    comments: Mapped[list["ReportComment"]] = relationship(
        "ReportComment",
        back_populates="commenter",
    )
