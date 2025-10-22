from fastapi import FastAPI, Depends, HTTPException
from schemas import CRUD_CREATE
from sqlalchemy.orm import Session
from database import SessionLocal,engine,Base
from models import CRUD
from schemas import CRUD_Response
from typing import List
Base.metadata.create_all(bind = engine)
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://preview--mui-redux-react.lovable.app", "*"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/crud",response_model=CRUD_Response)
def create_crud(crud: CRUD_CREATE, db: Session = Depends(get_db)):
      db_crud = CRUD(**crud.dict())
      db.add(db_crud)
      db.commit()
      db.refresh(db_crud)
      return db_crud

@app.get("/crud",response_model=List[CRUD_Response])
def get_crud(db: Session = Depends(get_db)):
    crud = db.query(CRUD).all()
    return crud

@app.get("/crud/{crud_id}",response_model=CRUD_Response)
def get_crud_by_id(crud_id: int, db: Session = Depends(get_db)):
    crud = db.query(CRUD).filter(CRUD.id == crud_id).first()
    if not crud:
        raise HTTPException(status_code=404, detail="CRUD not found")
    return crud

@app.put("/crud/{crud_id}",response_model=CRUD_Response)
def update_crud(crud_id: int, crud: CRUD_CREATE, db: Session = Depends(get_db)):
    db_crud = db.query(CRUD).filter(CRUD.id == crud_id).first()
    if not db_crud:
        raise HTTPException(status_code=404, detail="CRUD not found")
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
    crud = db.query(CRUD).filter(CRUD.id == crud_id).first()
    if not crud:
        raise HTTPException(status_code=404, detail="CRUD not found")
    db.delete(crud)
    db.commit()
    return {"message": "CRUD deleted successfully"}

@app.get("/crud/search",response_model=List[CRUD_Response])
def search_crud(query: str, db: Session = Depends(get_db)):
    crud = db.query(CRUD).filter(CRUD.name.ilike(f"%{query}%")).all()
    return crud

