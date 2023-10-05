from sqlalchemy import Boolean, Column, String, Integer
from ..config.database import Base


class UserSchema(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean, default=True)
    
class UserAdmSchema(Base):
    __tablename__ = "user_adm"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean, default=True)
    permission = Column(Boolean, default=False)
    
    
class UserMapped(UserSchema):
    pass
    
class UserAdmMapped(UserAdmSchema):
    pass
    
