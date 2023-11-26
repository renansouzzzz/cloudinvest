from sqlalchemy import Column, Integer, Numeric, ForeignKey, String, Boolean
from config.database import Base
from sqlalchemy.orm import relationship
    

class PortfolioSchema(Base):
    __tablename__ = 'portfolio'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id', onupdate='CASCADE'), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    total_balance = Column(Numeric(18,2), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    
    user = relationship('UserSchema', back_populates='portfolio')

    
class PortfolioMapped(PortfolioSchema):
    pass