from datetime import datetime
from pydantic import BaseModel, Field

from enum import Enum

class TagDatasPortfolio(Enum):
    Receitas = 0
    Despesas = 1
    Investimento = 2


class PortfolioDatas(BaseModel):
    name: str = Field(..., max_length=50)
    id_user: int
    value: float
    tag: TagDatasPortfolio
    expiration_day: int | None
    installment: int | None
    
    
class PortfolioDatasGetAll(PortfolioDatas):
    created_at: datetime = Field(default_factory=datetime.now)
    
class PortfolioDatasCreate(PortfolioDatas):
    pass

class PortfolioDatasUpdate(PortfolioDatas):
    pass