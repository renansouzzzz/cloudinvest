from sqlalchemy import Boolean, Column, String, Integer, Enum
from config.db.database import Base
from models.users.user import TypeProfileEnumDTO


class UserSchema(Base):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)

    
class UserMapped(UserSchema):
    type_profile: TypeProfileEnumDTO = Column(Enum(TypeProfileEnumDTO), nullable=True)  