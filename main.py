from fastapi import FastAPI, Depends, HTTPException  # FastAPI core imports for building the API
from schemas import CRUD_CREATE  # Request schema for creating/updating records
from sqlalchemy.orm import Session  # SQLAlchemy session type hint
from sqlalchemy import text  # For running raw SQL (used in lightweight migration)
from database import SessionLocal,engine,Base  # DB session factory, engine, and base model
from models import CRUD  # SQLAlchemy model
from schemas import CRUD_Response  # Response schema returned to clients
from typing import List
Base.metadata.create_all(bind = engine)  # Create tables if they don't exist yet
# Lightweight migration for new columns (PostgreSQL syntax)
# This attempts to add missing columns without requiring Alembic.
# If the DB doesn't support this exact syntax, the try/except makes it a no-op.
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE crud ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW() NOT NULL"))
        conn.execute(text("ALTER TABLE crud ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL"))
        conn.commit()
except Exception:
    # Skip if DB doesn't support this syntax; assume fresh create_all handled it
    pass
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware  # Enables cross-origin requests from the frontend

app.add_middleware(
    CORSMiddleware,
    # Allow your deployed frontend and any other origin (during development)
    allow_origins=["https://crudeducational.vercel.app/", "*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all request headers
)


def get_db():
    """Provide a database session to each request and close it afterwards."""
    db = SessionLocal()
    try:
        yield db  # Hand control back to the route with an open session
    finally:
        db.close()  # Make sure the session is closed

@app.post("/crud",response_model=CRUD_Response)
def create_crud(crud: CRUD_CREATE, db: Session = Depends(get_db)):
      """Create a new CRUD record."""
      db_crud = CRUD(**crud.dict())  # Convert validated Pydantic model into ORM object
      db.add(db_crud)
      db.commit()  # Persist to DB
      db.refresh(db_crud)  # Reload to include defaults like created_at
      return db_crud

@app.get("/crud",response_model=List[CRUD_Response])
def get_crud(db: Session = Depends(get_db)):
    """List all non-deleted records (soft-deletes are hidden)."""
    crud = db.query(CRUD).filter(CRUD.deleted_at.is_(None)).all()
    return crud

@app.get("/crud/{crud_id}",response_model=CRUD_Response)
def get_crud_by_id(crud_id: int, db: Session = Depends(get_db)):
    """Fetch a single record by its ID, ignoring soft-deleted ones."""
    crud = db.query(CRUD).filter(CRUD.id == crud_id, CRUD.deleted_at.is_(None)).first()
    if not crud:
        raise HTTPException(status_code=404, detail="CRUD not found")
    return crud

@app.put("/crud/{crud_id}",response_model=CRUD_Response)
def update_crud(crud_id: int, crud: CRUD_CREATE, db: Session = Depends(get_db)):
    """Update an existing record by ID (only if not soft-deleted)."""
    db_crud = db.query(CRUD).filter(CRUD.id == crud_id, CRUD.deleted_at.is_(None)).first()
    if not db_crud:
        raise HTTPException(status_code=404, detail="CRUD not found")
    # Apply incoming changes
    db_crud.name = crud.name
    db_crud.email = crud.email
    db_crud.phone = crud.phone
    db_crud.department = crud.department
    db_crud.year = crud.year
    db.commit()
    db.refresh(db_crud)
    return db_crud

@app.delete("/crud/{crud_id}",status_code=204)
def delete_crud(crud_id: int, db: Session = Depends(get_db)):
    """Soft delete by setting deleted_at; data remains for auditing/recovery."""
    crud = db.query(CRUD).filter(CRUD.id == crud_id, CRUD.deleted_at.is_(None)).first()
    if not crud:
        raise HTTPException(status_code=404, detail="CRUD not found")
    # Soft delete: set deleted_at using DB server time
    from sqlalchemy.sql import func as sa_func
    crud.deleted_at = sa_func.now()
    db.commit()
    return {"message": "CRUD deleted successfully"}

@app.get("/crud/search",response_model=List[CRUD_Response])
def search_crud(query: str, db: Session = Depends(get_db)):
    """Case-insensitive search on name, ignoring soft-deleted records."""
    crud = db.query(CRUD).filter(CRUD.deleted_at.is_(None), CRUD.name.ilike(f"%{query}%")).all()
    return crud

