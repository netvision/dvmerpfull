import os
import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

# Load .env so DATABASE_URL and SECRET_KEY are available
load_dotenv(Path(__file__).parent.parent / ".env")

# Allow imports from the backend package root
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Base, DATABASE_URL  # noqa: E402
import models  # noqa: F401 — registers all ORM models with Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Point Alembic at our app's metadata for autogenerate
target_metadata = Base.metadata

# Override the ini url with the env-driven one
config.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
