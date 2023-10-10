from pydantic import BaseModel

class Portfolio(BaseModel):
    name: str
    id_user: int
    current_balace: float
    total_balance: float
    installment: int
    
class PortfolioCreate(Portfolio):
    pass

class PortfolioUpdate(Portfolio):
    pass