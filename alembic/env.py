# alembic/env.py

import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.exc import SQLAlchemyError
import getpass
from sqlalchemy.engine.url import URL
from logging.config import fileConfig
import logging

sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
print("Alembic is executing env.py")

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

logger = logging.getLogger('alembic')

target_metadata = Base.metadata

def run_migrations_offline(db_url):
    print("Running migrations in offline mode.")
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online(db_url):
    print("Running migrations in online mode.")
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
                compare_type=True,
            )

            with context.begin_transaction():
                context.run_migrations()
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Parse custom command-line arguments
cmd_opts = context.get_x_argument(as_dictionary=True)
migration_mode = cmd_opts.get('mode', None)
db_url = cmd_opts.get('db_url', None)

if migration_mode == 'online':
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
    run_migrations_online(str(db_url))
elif migration_mode == 'offline':
    db_url = db_url or "sqlite:///./test.db"
    run_migrations_offline(db_url)
else:
    if context.is_offline_mode():
        db_url = db_url or "sqlite:///./test.db"
        run_migrations_offline(db_url)
    else:
        # For online mode, prompt for password if db_url is not provided
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
        run_migrations_online(str(db_url))
