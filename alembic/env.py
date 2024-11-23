import os
import sys
import logging
import getpass
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import URL
from logging.config import fileConfig
from sqlalchemy.exc import SQLAlchemyError

# Include application modules in the path
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

# Load Alembic configuration
config = context.config
fileConfig(config.config_file_name)

# Setup logger
logger = logging.getLogger("alembic")

# Import Base and models to include metadata
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
from database.scrapes.cardratings import CardratingsScrape
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

def get_db_url():
    """Generate the database URL based on the mode and user input."""
    # If db_url is provided via `-x` arguments, use it
    cmd_opts = context.get_x_argument(as_dictionary=True)
    db_url = cmd_opts.get("db_url")

    # Prompt for password if no db_url is provided
    if db_url is None:
        db_password = getpass.getpass("Enter database password: ")
        db_url = URL.create(
            drivername="postgresql+psycopg2",
            username="cardmathdb",
            password=db_password,
            host="34.31.74.189",
            port=5432,
            database="postgres",
            query={
                "sslmode": "verify-ca",
                "sslrootcert": "/home/johannes/cloudsql_keys/server-ca.pem",
                "sslcert": "/home/johannes/cloudsql_keys/client-cert.pem",
                "sslkey": "/home/johannes/cloudsql_keys/client-key.pem",
            },
        )
    return str(db_url)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    print("Running migrations in offline mode.")
    db_url = get_db_url()
    context.configure(
        connection=db_url,
        target_metadata=target_metadata,
        compare_type=True,  # Compare column types
        compare_server_default=True,  # Compare server default values
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    print("Running migrations in online mode.")
    db_url = get_db_url()

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


# Run migrations based on the mode (online or offline)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
