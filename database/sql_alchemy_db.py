import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

ENVIRONMENT = os.getenv("ENVIRONMENT", "prod")

if ENVIRONMENT == "prod":
    # Production configuration (Google Cloud SQL)
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "cardmathdb")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_database_password")
    DB_HOST = os.getenv("DB_HOST", "cardmath-llc:us-central1:cardmathdb")  # Instance connection name
    HOST_PREFIX = "/cloudsql"

    # SQLAlchemy database URLs for async and sync connections
    SQLALCHEMY_DATABASE_URL_ASYNC = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={HOST_PREFIX}/{DB_HOST}"
    SQLALCHEMY_DATABASE_URL_SYNC = f"postgresql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={HOST_PREFIX}/{DB_HOST}"

else:
    # Local development configuration (SQLite)
    SQLALCHEMY_DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./test.db?check_same_thread=False"
    SQLALCHEMY_DATABASE_URL_SYNC = "sqlite:///./test.db?check_same_thread=False"

# Create asynchronous and synchronous SQLAlchemy engines
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)
sync_engine = create_engine(SQLALCHEMY_DATABASE_URL_SYNC)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

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
