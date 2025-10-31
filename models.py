from sys import dont_write_bytecode
from database import Base  # Base class for all SQLAlchemy models
from sqlalchemy import Column, Integer, String, DateTime  # Column types
from sqlalchemy.sql import func  # DB-side functions like NOW()

class CRUD(Base):
    # Physical table name in the database
    __tablename__ = "crud"

    # Primary key identifier
    id = Column(Integer, primary_key=True, index=True)

    # Basic profile fields
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    department = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    # Audit fields
    created_at = Column(
        DateTime(timezone=False),  # Stored as naive timestamp (UTC recommended)
        server_default=func.now(),  # Let the DB set current timestamp
        nullable=False,
    )
    deleted_at = Column(
        DateTime(timezone=False),  # Null means not deleted (soft delete)
        nullable=True,
    )