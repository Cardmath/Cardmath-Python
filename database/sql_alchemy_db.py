import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

# Load environment variables for PostgreSQL connection
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "cardmathdb")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_database_password")
DB_HOST = os.getenv("DB_HOST", "cardmath-llc:us-central1:cardmathdb")  # Use the instance connection name only

# SQLAlchemy database URLs for async and sync connections
SQLALCHEMY_DATABASE_URL_ASYNC = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host=/cloudsql/{DB_HOST}"
SQLALCHEMY_DATABASE_URL_SYNC = f"postgresql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host=/cloudsql/{DB_HOST}"

# Create asynchronous and synchronous SQLAlchemy engines
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)
sync_engine = create_engine(SQLALCHEMY_DATABASE_URL_SYNC)

# Configure session factories for async and sync usage
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

# Declare base class for models
Base = declarative_base()

# Async generator for database session (for async use)
async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()  # Close the session asynchronously

# Sync generator for database session (for sync use)
def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()  # Close the session synchronously

# Function to print the SQL schema
def print_sql_schema(out_name='schema.sql'):
    output_file = out_name
    with open(output_file, 'w') as file:
        for table in Base.metadata.sorted_tables:
            sql = str(CreateTable(table).compile(sync_engine))  # Use the sync engine for schema printing
            file.write(sql)
            file.write("\n\n")  # Add extra newline for separation between tables
    print(f"SQL schema has been written to {output_file}")
