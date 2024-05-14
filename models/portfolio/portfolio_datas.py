from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from enum import Enum


class TagDatasPortfolio(Enum):
    Receitas = 0
    Despesas = 1
    Investimentos = 2


class PortfolioDatas(BaseModel):
    name: str = Field(..., max_length=50)
    id_user: int
    value: float
    tag: TagDatasPortfolio
    expiration_day: int | None
    installment: int | None
    is_recurring: bool


class PortfolioDatasGetAll(PortfolioDatas):
    created_at: datetime = Field(default_factory=datetime.now)


class PortfolioDatasCreate(PortfolioDatas):
    pass


class PortfolioDatasUpdate(PortfolioDatas):
    pass
