import datetime

from MySQLdb import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from config.database import engine

from schemas.portfolio_datas import PortfolioDatasMapped, PortfolioDatasSchema
from schemas.port_installments import PortfolioDatasInstallmentsMapped
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
        start_date = f'{year}-{monthStr[0]}-01 00:00:00:0000'
        end_date = f'{year}-{monthStr[0]}-{monthStr[1]} 23:59:59:9999'

        data = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.id_user == idUser,
                PortfolioDatasMapped.created_at.between(start_date, end_date)
            )
        ).all()

        if data is None:
            raise ValueError(f'Nenhum dado foi encontrado!')
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
            portfolio_datas = PortfolioDatasMapped(**payload.dict())

            session.add(portfolio_datas)
            session.commit()
            session.refresh(portfolio_datas)

            installment_value = portfolio_datas.value / portfolio_datas.installment

            installment_dates = []
            current_date = datetime.date(
                datetime.datetime.today().year, datetime.datetime.today().month - 1, portfolio_datas.expiration_day
            )

            for i in range(portfolio_datas.installment):
                days_in_month = ParseToTypes.parseMonthToDays(current_date.month)
                current_date += datetime.timedelta(days=days_in_month)
                installment_dates.append(current_date)

            for i, date in enumerate(installment_dates):
                installment = PortfolioDatasInstallmentsMapped(
                    id_user=portfolio_datas.id_user,
                    id_port_datas=portfolio_datas.id,
                    current_installment=i + 1,
                    value_installment=installment_value,
                    created_at=datetime.datetime.now(),
                    expiration_date=date
                )
                session.add(installment)
                session.commit()

        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Error on database: {e}")

        return True


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
