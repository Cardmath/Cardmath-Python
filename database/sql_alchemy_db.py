from auth.secrets import load_secret
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

Base = declarative_base()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DB_NAME = None
if ENVIRONMENT == "prod":
    DB_NAME = os.getenv("DB_NAME", "postgres")
    print("Using prod database")
else :
    DB_NAME = os.getenv("DB_NAME", "postgres_dev")
    print("Using development database")

DB_USER = "postgres"
DB_PASSWORD = load_secret(secret_name="db_password", set_env=False)
if not DB_PASSWORD or len(DB_PASSWORD) == 0:
    raise Exception(f"DB Password not set!")

DB_HOST = os.getenv("DB_HOST", "cardmath-llc:northamerica-northeast2:cardmathdb")
HOST_PREFIX = "/cloudsql"

SQLALCHEMY_DATABASE_URL_SYNC = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?"
    f"host={HOST_PREFIX}/{DB_HOST}"
)

sync_engine = create_engine(SQLALCHEMY_DATABASE_URL_SYNC)

SyncSessionGenerator = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

def get_sync_db():
    db = SyncSessionGenerator()
    try:
        yield db
    finally:
        db.close()