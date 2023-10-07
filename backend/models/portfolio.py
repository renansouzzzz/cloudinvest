from sqlalchemy import Column, Integer, Numeric, ForeignKey
from ..config.database import Base
    

class PortfolioSchema(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    id_user = Column(ForeignKey('user.id'), nullable=False)
    total_balance = Column(Numeric(18,2), nullable=False)
    
    
class PortfolioMapped(PortfolioSchema): 
    pass