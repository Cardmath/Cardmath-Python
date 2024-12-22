from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from auth.secrets import load_secret
from sqlalchemy.schema import CreateTable
import os

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

SQLALCHEMY_DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?"
    f"host={HOST_PREFIX}/{DB_HOST}"
)
SQLALCHEMY_DATABASE_URL_SYNC = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?"
    f"host={HOST_PREFIX}/{DB_HOST}"
)

sync_engine = create_engine(SQLALCHEMY_DATABASE_URL_SYNC)

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

Base = declarative_base()

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

def print_sql_schema(out_name='schema.sql'):
    output_file = out_name
    with open(output_file, 'w') as file:
        for table in Base.metadata.sorted_tables:
            sql = str(CreateTable(table).compile(sync_engine))  # Use the sync engine for schema printing
            file.write(sql)
            file.write("\n\n")
    print(f"SQL schema has been written to {output_file}")
