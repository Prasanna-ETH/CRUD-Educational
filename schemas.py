from os import name  # Unused import kept if referenced elsewhere
from typing import Optional  # For optional fields in responses
from datetime import datetime  # Timestamp fields
from pydantic import BaseModel, EmailStr, Field  # Pydantic model base and field types

class CRUD_BASE(BaseModel):
    # Person/record name; allows spaces and common punctuation
    name: str = Field(min_length=2, max_length=50, pattern=r"^[A-Za-z\s.'-]+$")
    # RFC-compliant email validation (requires email-validator)
    email: EmailStr
    # Phone with optional +, spaces, dashes, parentheses
    phone: str = Field(min_length=7, max_length=20, pattern=r"^\+?[0-9\s\-()]{7,20}$")
    # Department or course name; letters, spaces, ampersand and punctuation
    department: str = Field(min_length=2, max_length=50, pattern=r"^[A-Za-z\s&.'-]+$")
    # Year within 1..10 (adjust as needed)
    year: int = Field(ge=1, le=10)

class CRUD_CREATE(CRUD_BASE):
    # Inherits all validation rules for creation
    pass

class CRUD_Response(CRUD_BASE):
    # Server-assigned database ID
    id: int
    # When the row was created (server time)
    created_at: datetime
    # Null when active, timestamp when soft-deleted
    deleted_at: Optional[datetime] = None
    class Config:
        # Allow constructing from ORM objects
        from_attributes = True