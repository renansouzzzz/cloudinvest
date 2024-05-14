from sqlalchemy import Boolean, Column, String, Integer
from config.db.database import Base


class UserAdmSchema(Base):
    __tablename__ = 'user_adm'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)
    permission = Column(Boolean, default=False)
    

class UserAdmMapped(UserAdmSchema):
    pass