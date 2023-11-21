from pydantic import BaseModel

class Portfolio(BaseModel):
    name: str
    id_user: int
    total_balance: float
    
    
class PortfolioCreate(Portfolio):
    pass

class PortfolioUpdate(Portfolio):
    pass