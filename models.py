from sys import dont_write_bytecode
from database import Base
from sqlalchemy import Column, Integer, String , Boolean

class CRUD(Base):
    __tablename__ = "crud"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    department = Column(String, nullable=False)
    year = Column(Integer, nullable=False)