from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.database import engine
from schemas.port_installments import PortfolioDatasInstallmentsSchema, PortfolioDatasInstallmentsMapped
from utils.parse_types import ParseToTypes


def getAll():
    with Session(engine) as session:
        data = session.query(PortfolioDatasInstallmentsSchema).all()
        if data is None:
            raise ValueError(f'Nada encontrado!')
        return data


def getByDate(idUser: int, month: str, year: int):
    with Session(engine) as session:
        monthStr = ParseToTypes.parseMonthToStr(month)
        start_date = f'{year}-{monthStr[0]}-01 00:00:00:0000'
        end_date = f'{year}-{monthStr[0]}-{monthStr[1]} 23:59:59:9999'

        data = session.query(PortfolioDatasInstallmentsMapped).filter(
            and_(
                PortfolioDatasInstallmentsMapped.id_user == idUser,
                PortfolioDatasInstallmentsMapped.expiration_date.between(start_date, end_date)
            )
        ).all()

        if data is None:
            raise ValueError('Nenhum dado foi encontrado!')
        return data
