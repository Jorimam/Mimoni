from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, text
from typing import Optional


class Expenses(SQLModel, table=True):
    __tablename__ = "expenses"

    id: Optional[int] = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        nullable=False
    )
    description: str = Field(max_length=255, nullable=False)
    category: str = Field(max_length=100, index=True, nullable=False)
    
    # Decimal/Numeric configurations pass down accurately via sa_type
    amount: Decimal = Field(max_digits=12, decimal_places=2, nullable=False)
    
    # Timestamps using server-side hooks pass down smoothly via sa_column_kwargs
    created_at: datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
            "nullable": False
        }
    )
