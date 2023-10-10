from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..config.database import Base, engine

from ..schemas.portfolio import PortfolioMapped, PortfolioSchema
        
app = FastAPI()

Base.metadata.create_all(engine)


def get(id : int):
    with Session(engine) as session:
        return session.get(PortfolioSchema, id)
    
def create(payload: PortfolioSchema):
    with Session(engine) as session:
        portfolio = PortfolioMapped(**payload.dict())
        session.add(portfolio)
        session.commit()
        session.refresh(portfolio)
        return portfolio