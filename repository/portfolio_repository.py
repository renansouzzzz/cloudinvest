from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from config.database import engine

from schemas.portfolio import PortfolioMapped, PortfolioSchema


def getById(id : int):
    with Session(engine) as session:
        data = session.get(PortfolioMapped, id)
        if data is None:
            raise ValueError(f'O usuário com ID {id} não foi encontrado!')
        return data
        
    
def create(payload: PortfolioSchema):
    with Session(engine) as session:
        try:
            portfolio = PortfolioMapped(**payload.dict())
        
            session.add(portfolio)
            session.commit()
            session.refresh(portfolio)    
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Error: {e}")
        
        return portfolio