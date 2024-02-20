from sqlalchemy import Column, Integer, Numeric, ForeignKey, String, Boolean
from config.database import Base
from sqlalchemy.orm import relationship
    

class PortfolioSchema(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id', onupdate='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    total_balance = Column(Numeric(18,2), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    
    user = relationship('UserSchema')
    
        
class PortfolioMapped(PortfolioSchema):
    pass