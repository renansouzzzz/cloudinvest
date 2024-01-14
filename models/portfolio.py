from pydantic import BaseModel, Field

class Portfolio(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    id_user: int
    total_balance: float
    
    
class PortfolioCreate(Portfolio):
    pass

class PortfolioUpdate(Portfolio):
    pass