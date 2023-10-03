from sqlalchemy import Boolean, Column, String, Integer
from ..config.database import Base
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    
class UserTeste(User):
    pass
    
    
