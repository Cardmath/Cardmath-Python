from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateTable

SQLALCHEMY_DATABASE_URL = "sqlite:///./cardmath.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def print_sql_schema(out_name='schema.sql'):
    # Define the output file path
    output_file = out_name

    # Open the file in write mode
    with open(output_file, 'w') as file:
        # Write the generated SQL for each table into the file
        for table in Base.metadata.sorted_tables:
            sql = str(CreateTable(table).compile(engine))
            file.write(sql)
            file.write("\n\n")  # Add extra newline for separation between tables

    print(f"SQL schema has been written to {output_file}")