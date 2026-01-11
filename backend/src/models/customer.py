"""顧客モデル定義。"""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .visit_record import VisitRecord


class Customer(Base, TimestampMixin):
    """顧客モデル。"""

    __tablename__ = "CUSTOMER"

    customer_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    company_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    contact_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, index=True
    )

    # 訪問記録とのリレーション
    visit_records: Mapped[list["VisitRecord"]] = relationship(
        "VisitRecord",
        back_populates="customer",
    )
