from sqlalchemy import Column, Integer, String, func, DateTime, Float, Numeric
from datetime import datetime
from ..base import Base


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    description = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )