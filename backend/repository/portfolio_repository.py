from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..config.database import Base, engine

from ..models.portfolio import PortfolioMapped, PortfolioSchema
        
app = FastAPI()

Base.metadata.create_all(engine)


def get(id : int):
    with Session(engine) as session:
        
        return session.get(PortfolioSchema, id)