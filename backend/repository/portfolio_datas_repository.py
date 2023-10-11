from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..config.database import Base, engine

from ..schemas.portfolio_datas import PortfolioDatasMapped, PortfolioDatasSchema
        
app = FastAPI()

Base.metadata.create_all(engine)


def get():
    with Session(engine) as session:
        return session.query(PortfolioDatasMapped).all()  
    
def create(payload: PortfolioDatasSchema):
    with Session(engine) as session:
        portfolioDatas = PortfolioDatasMapped(**payload.dict())
        session.add(portfolioDatas)
        session.commit()
        session.refresh(portfolioDatas)
        return portfolioDatas