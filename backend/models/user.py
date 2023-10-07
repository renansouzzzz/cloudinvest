from sqlalchemy import Boolean, Column, String, Integer, Enum
from ..config.database import Base
from ..schemas.user import TypeProfileEnumDTO


class UserSchema(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(18), nullable=False)
    active = Column(Boolean, default=True)
    type_profile: TypeProfileEnumDTO = Column(Enum(TypeProfileEnumDTO))
    
    
class UserMapped(UserSchema):
    pass  