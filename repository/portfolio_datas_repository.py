from MySQLdb import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from config.database import engine

from schemas.portfolio_datas import PortfolioDatasMapped, PortfolioDatasSchema
        

def getAll(idUser: int):
    with Session(engine) as session:
        data = session.query(PortfolioDatasMapped).filter(PortfolioDatasMapped.id_user == idUser).all()
        if data is None:
            raise ValueError(f'Nenhum usuário foi encontrado!')
        return data
    
def getById(id: int):
    with Session(engine) as session:
        data = session.get(PortfolioDatasMapped, id)
        if data is None:
            raise ValueError(f'O usuário com ID {id} não foi encontrado!')
        return data 
    
def create(payload: PortfolioDatasSchema):
    with Session(engine) as session:
        try:    
            portfolioDatas = PortfolioDatasMapped(**payload.dict())
            
            session.add(portfolioDatas)
            session.commit()
            session.refresh(portfolioDatas)
        
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Error on database: {e}")
            
        return portfolioDatas
    
def delete(id: int):
    with Session(engine) as session:
        try:
            getPortfolioData = session.get(PortfolioDatasSchema, id)
            
            if not getPortfolioData:
                raise HTTPException(status_code=404, detail="Informação não encontrada!")
            
            session.delete(getPortfolioData)
            session.commit()
             
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f'Error on database: {e}')
             
        return "Informação deletada com sucesso!"