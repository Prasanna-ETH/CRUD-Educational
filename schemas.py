from os import name
from pydantic import BaseModel

class CRUD_BASE(BaseModel):
    name: str
    email: str
    phone: str
    department: str
    year: int

class CRUD_CREATE(CRUD_BASE):
    pass

class CRUD_Response(CRUD_BASE):
    id: int
    class Config:
        from_attributes = True