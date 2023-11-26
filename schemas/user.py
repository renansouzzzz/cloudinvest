from sqlalchemy import Boolean, Column, String, Integer, Enum
from config.database import Base
from models.user import TypeProfileEnumDTO
from sqlalchemy.orm import relationship


class UserSchema(Base):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(18), nullable=False)
    active = Column(Boolean, default=True)
    
    
    portfolio_datas = relationship('PortfolioDatasSchema', back_populates='user', cascade='all, delete', passive_deletes=True)
    portfolio = relationship('PortfolioSchema', back_populates='user', cascade='all, delete', passive_deletes=True)

    
class UserMapped(UserSchema):
    type_profile: TypeProfileEnumDTO = Column(Enum(TypeProfileEnumDTO), nullable=True)  