from MySQLdb import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from config.database import engine

from schemas.portfolio_datas import PortfolioDatasMapped, PortfolioDatasSchema
from utils.parse_types import ParseToTypes
        

def getAll(idUser: int):
    with Session(engine) as session:
        data = session.query(PortfolioDatasMapped).filter(PortfolioDatasMapped.id_user == idUser).all()
        if data is None:
            raise ValueError(f'Nenhum usuário foi encontrado!')
        return data
    
def getByDate(idUser: int, month: str, year: int):
    with Session(engine) as session:
        monthStr = ParseToTypes.parseMonthToStr(month)
        data = session.query(PortfolioDatasMapped).filter(
            PortfolioDatasMapped.id_user == idUser and PortfolioDatasMapped.created_at.between(f'{year}-{monthStr[0]}-01', f'{year}-{monthStr[0]}-{monthStr[1]}')
        ).all()
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