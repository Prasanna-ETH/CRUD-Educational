from sqlalchemy import create_engine  # Creates the connection to the database
from sqlalchemy.orm import sessionmaker, declarative_base  # Session factory and model base
import os  # Read environment variables
from dotenv import load_dotenv  # Load .env file values

# Load variables from .env into the environment
load_dotenv()

# Example: postgresql+psycopg2://user:pass@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a reusable engine; SQLAlchemy manages connection pooling
engine = create_engine(DATABASE_URL)

# SessionLocal() gives a new database session for each request
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class to inherit from for model declarations
Base = declarative_base()