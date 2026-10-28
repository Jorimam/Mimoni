from datetime import datetime
from sqlmodel import SQLModel, Field, text
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(
        default=None, 
        primary_key=True, 
        nullable=False
    )
    full_name: str = Field(max_length=255, nullable=False)
    username: str = Field(max_length=255, unique=True, index=True, nullable=False)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)

    # Replaces the Mixin for clean tracking under SQLModel meta-engines
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

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
