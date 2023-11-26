from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from config.database import engine

from schemas.portfolio import PortfolioMapped, PortfolioSchema


def get(id : int):
    with Session(engine) as session:
        return session.get(PortfolioSchema, id)
    
def create(payload: PortfolioSchema):
    with Session(engine) as session:
        try:
            portfolio = PortfolioMapped(**payload.dict())
            
            session.add(portfolio)
            session.commit()
            session.refresh(portfolio)    
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Chave estrangeira não encontrada")
        
        
        return portfolio