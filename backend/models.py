from sqlalchemy import Boolean, Column, String
from .config.database import Base
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class User(Base):
    __tablename__ = "users"
    
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    
class UserTeste(User):
    pass
    
    
