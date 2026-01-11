"""日報コメントモデル定義。"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .daily_report import DailyReport
    from .salesperson import Salesperson


class ReportComment(Base):
    """日報コメントモデル。

    日報に対するコメント。上長や本人が複数コメントを投稿可能。
    """

    __tablename__ = "REPORT_COMMENT"

    comment_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    report_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("DAILY_REPORT.report_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    commenter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("SALESPERSON.salesperson_id"),
        nullable=False,
        index=True,
    )
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    # 日報とのリレーション
    daily_report: Mapped["DailyReport"] = relationship(
        "DailyReport",
        back_populates="comments",
    )

    # コメント投稿者とのリレーション
    commenter: Mapped["Salesperson"] = relationship(
        "Salesperson",
        back_populates="comments",
    )
