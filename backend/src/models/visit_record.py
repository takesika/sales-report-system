"""訪問記録モデル定義。"""

from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .customer import Customer
    from .daily_report import DailyReport


class VisitRecord(Base, TimestampMixin):
    """訪問記録モデル。

    日報に紐づく訪問記録。1日報に対して複数の訪問記録を登録可能。
    """

    __tablename__ = "VISIT_RECORD"

    visit_id: Mapped[int] = mapped_column(
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
    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("CUSTOMER.customer_id"),
        nullable=False,
        index=True,
    )
    visit_content: Mapped[str] = mapped_column(Text, nullable=False)
    visit_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # 日報とのリレーション
    daily_report: Mapped["DailyReport"] = relationship(
        "DailyReport",
        back_populates="visit_records",
    )

    # 顧客とのリレーション
    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="visit_records",
    )
