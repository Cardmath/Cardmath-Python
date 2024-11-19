# alembic/env.py

import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

from database.sql_alchemy_db import Base

from database.auth.user import (
    Account,
    Enrollment,
    Subscription,
    user_credit_card_association,
    User,
    UserInDB,
    wallet_card_association,
    Wallet
)
from database.creditcard.creditcard import CreditCard
from database.scrapes.cardratings import CardratingsScrape
from database.teller.preferences import (
    BanksPreferences,
    BusinessPreferences,
    ConsumerPreferences,
    ConsumerPreferences,
    CreditProfilePreferences,
    RewardsProgramsPreferences,
    Preferences
)
from database.teller.transactions import (
    Transaction,
    TransactionDetails,
    Counterparty
)

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
config.set_main_option("sqlalchemy.url", DB_URL)

def run_migrations_offline():
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
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
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
