"""日報モデル定義。"""

import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .report_comment import ReportComment
    from .salesperson import Salesperson
    from .visit_record import VisitRecord


class ReportStatus(enum.Enum):
    """日報ステータス。"""

    DRAFT = "draft"  # 下書き
    SUBMITTED = "submitted"  # 提出済
    CONFIRMED = "confirmed"  # 確認済


class DailyReport(Base, TimestampMixin):
    """日報モデル。

    営業担当者ごと・日付ごとに1レコードを持つ。
    """

    __tablename__ = "DAILY_REPORT"
    __table_args__ = (
        UniqueConstraint("salesperson_id", "report_date", name="UK_DAILY_REPORT_DATE"),
    )

    report_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    salesperson_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("SALESPERSON.salesperson_id"),
        nullable=False,
    )
    report_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    problem: Mapped[str | None] = mapped_column(Text, nullable=True)
    plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=ReportStatus.DRAFT,
        index=True,
    )

    # 営業担当者とのリレーション
    salesperson: Mapped["Salesperson"] = relationship(
        "Salesperson",
        back_populates="daily_reports",
    )

    # 訪問記録とのリレーション
    visit_records: Mapped[list["VisitRecord"]] = relationship(
        "VisitRecord",
        back_populates="daily_report",
        cascade="all, delete-orphan",
    )

    # コメントとのリレーション
    comments: Mapped[list["ReportComment"]] = relationship(
        "ReportComment",
        back_populates="daily_report",
        cascade="all, delete-orphan",
    )
