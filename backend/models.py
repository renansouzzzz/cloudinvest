from sqlalchemy import Boolean, Column, Integer, String
from .config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    hash_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    
