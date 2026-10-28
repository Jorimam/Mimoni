import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlmodel import SQLModel
target_metadata = SQLModel.metadata

from app.models import model_expenses, users

from app.base import Base
from app.database import SQLALCHEMY_DB_URL
from app import models  # noqa: F401  (registers the tables on Base.metadata)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=SQLALCHEMY_DB_URL.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Explicitly casting URL to string to avoid connection engine initialization problems
    connectable = create_engine(
        SQLALCHEMY_DB_URL.render_as_string(hide_password=False), 
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()