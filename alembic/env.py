import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from database.sql_alchemy_db import Base

# Load Alembic config and logger
config = context.config
fileConfig(config.config_file_name)

# Set the metadata for migrations
target_metadata = Base.metadata

# Get the database URL dynamically
DB_URL = os.getenv("SQLALCHEMY_DATABASE_URL_SYNC", "sqlite:///./test.db")
config.set_main_option("sqlalchemy.url", DB_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
