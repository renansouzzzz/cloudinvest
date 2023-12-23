from fastapi import HTTPException
from sqlalchemy.orm import Session

from config.database import engine

from schemas.portfolio_datas import PortfolioDatasMapped, PortfolioDatasSchema
        

def get():
    with Session(engine) as session:
        return session.query(PortfolioDatasMapped).all()  
    
def getById(id: int):
    with Session(engine) as session:
        return session.get(PortfolioDatasMapped, id) 
    
def create(payload: PortfolioDatasSchema):
    with Session(engine) as session:
        
        portfolioDatas = PortfolioDatasMapped(**payload.dict())
        
        session.add(portfolioDatas)
        session.commit()
        session.refresh(portfolioDatas)
        
        return portfolioDatas
    
def delete(int: id):
    with Session(engine) as session:
        
        getPortfolioData = session.get(PortfolioDatasSchema, id)
        
        if not getPortfolioData:
            raise HTTPException(status_code=404, detail="Informação não encontrada!")
        
        session.execute(f"UPDATE port_datas SET active = false WHERE id = {id}")
        session.commit() 
         
        return "Informação deletada com sucesso!"