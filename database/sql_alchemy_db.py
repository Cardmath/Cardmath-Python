from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

SQLALCHEMY_DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./cardmath.db"
SQLALCHEMY_DATABASE_URL_SYNC = "sqlite:///./cardmath.db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC, connect_args={"check_same_thread": False})

sync_engine = create_engine(SQLALCHEMY_DATABASE_URL_SYNC, connect_args={"check_same_thread": False})
with sync_engine.connect() as connection:
    connection.execute("PRAGMA journal_mode=WAL;")

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

# Base for both sync and async engines
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


def print_sql_schema(out_name='schema.sql'):
    # Define the output file path
    output_file = out_name

    # Open the file in write mode
    with open(output_file, 'w') as file:
        # Write the generated SQL for each table into the file
        for table in Base.metadata.sorted_tables:
            sql = str(CreateTable(table).compile(sync_engine))  # Use the sync engine for schema printing
            file.write(sql)
            file.write("\n\n")  # Add extra newline for separation between tables

    print(f"SQL schema has been written to {output_file}")