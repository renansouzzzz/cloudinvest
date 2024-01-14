from pydantic import BaseModel, Field

from enum import Enum

class TagDatasPortfolio(Enum):
    RendaMensal = 0
    DespesasMensais = 1
    DividasRecorrentes = 2
    DividasEmAtraso = 3

class PortfolioDatas(BaseModel):
    name: str = Field(..., max_length=50)
    id_portfolio: int
    value: float
    tag: TagDatasPortfolio
    installment: int
    
    
class PortfolioDatasCreate(PortfolioDatas):
    pass

class PortfolioDatasUpdate(PortfolioDatas):
    pass