import os
import sys
import logging
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import URL
from logging.config import fileConfig
from sqlalchemy.exc import SQLAlchemyError
from database.sql_alchemy_db import SQLALCHEMY_DATABASE_URL_SYNC

# Include application modules in the path
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

# Load Alembic configuration
config = context.config
fileConfig(config.config_file_name)

# Setup logger
logger = logging.getLogger("alembic")

from database.sql_alchemy_db import Base
target_metadata = Base.metadata
from database.auth.user import (
    Account,
    Enrollment,
    Subscription,
    user_credit_card_association,
    User,
    UserInDB,
    wallet_card_association,
    Wallet,
)
from database.creditcard.creditcard import CreditCard
from database.creditcard.source import CreditCardSource, CreditCardUpdateTaskQueue, register_update_insert_trigger, insert_update_sql
from database.teller.preferences import (
    BanksPreferences,
    BusinessPreferences,
    ConsumerPreferences,
    CreditProfilePreferences,
    RewardsProgramsPreferences,
    Preferences,
)
from database.teller.transactions import Transaction, TransactionDetails, Counterparty

print("Tables in target_metadata:")
print(target_metadata.tables.keys())

def run_migrations_online():
    """Run migrations in 'online' mode."""
    print("Running migrations in online mode.")
    db_url = SQLALCHEMY_DATABASE_URL_SYNC

    try:
        connectable = engine_from_config(
            {"sqlalchemy.url": db_url},
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,  # Compare column types
                compare_server_default=True,  # Compare server default values
                include_schemas=True
            )

            with context.begin_transaction():
                context.run_migrations()
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


run_migrations_online()
