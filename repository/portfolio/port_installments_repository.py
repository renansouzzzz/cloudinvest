from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, or_, extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.db.database import engine
from models.portfolio.portfolio_datas import TagDatasPortfolio
from models.portfolio.unified_all_portfolio_data import UnifiedAllPortfolioData
from models.portfolio.unified_some_portfolio_data import UnifiedSomePortfolioData
from schemas.portfolio.port_installments import PortfolioDatasInstallmentsSchema, PortfolioDatasInstallmentsMapped
from schemas.portfolio.portfolio_datas import PortfolioDatasMapped
from utils.parse_types import ParseToTypes


def getAll():
    with Session(engine) as session:
        data = session.query(PortfolioDatasInstallmentsSchema).all()
        if data is None:
            raise ValueError(f'Nada encontrado!')
        return data


def getByDate(idUser: int, month: str, year: int):
    with Session(engine) as session:
        try:
            monthStr = ParseToTypes.parseMonthToStr(month)

            start_date = datetime(year, int(monthStr[0]), 1, 0, 0, 0, 0)
            end_date = datetime(year, int(monthStr[0]), int(monthStr[1]), 23, 59, 59, 9999)

            data = session.query(PortfolioDatasInstallmentsMapped, PortfolioDatasMapped). \
                join(PortfolioDatasMapped,
                     and_(PortfolioDatasMapped.id == PortfolioDatasInstallmentsMapped.id_port_datas,
                          PortfolioDatasMapped.id_user == idUser)). \
                filter(
                or_(
                    and_(
                        PortfolioDatasMapped.is_recurring == True,
                        extract('year', PortfolioDatasMapped.created_at) <= year,
                        extract('month', PortfolioDatasMapped.created_at) <= int(monthStr[0])
                    ),
                    PortfolioDatasInstallmentsMapped.expiration_date.between(start_date, end_date)
                ),
                PortfolioDatasInstallmentsMapped.id_user == idUser
            ). \
                all()

            if data is None:
                raise ValueError('Nenhum dado foi encontrado!')

            unified_list = []

            for port_installment, port_data in data:
                unified_datas = UnifiedAllPortfolioData(
                    id=port_installment.id,
                    idPortData=port_data.id,
                    name=port_data.name,
                    installment=port_data.installment,
                    current_installment=port_installment.current_installment,
                    expiration_date=port_installment.expiration_date,
                    created_at=port_data.created_at,
                    idUser=port_data.id_user,
                    expiration_day=port_data.expiration_day,
                    value_installment=port_installment.value_installment,
                    value=port_data.value,
                    tag=port_data.tag,
                    is_recurring=port_installment.is_recurring,
                    is_paid=port_installment.is_paid
                )
                unified_list.append(unified_datas)

        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f'Error on database: {e}')

        return unified_list
    

def invoicePaid(idInstallment: int):
    with Session(engine) as session:
        try:
            data = session.query(PortfolioDatasInstallmentsMapped).filter(
                PortfolioDatasInstallmentsMapped.id == idInstallment).first()

            if data is None:
                raise ValueError('Nenhum dado foi encontrado!')

            data.is_paid = not data.is_paid

            session.commit()
            session.refresh(data)

        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f'Error on database: {e}')

        return data.is_paid


def calculatePortfolioBalanceInstallments(idUser: int, month: str, year: int):
    with Session(engine) as session:

        total_revenues = 0
        total_expenses = 0

        monthStr = ParseToTypes.parseMonthToStr(month)

        start_date = datetime(year, int(monthStr[0]), 1, 0, 0, 0, 0)
        end_date = datetime(year, int(monthStr[0]), int(monthStr[1]), 23, 59, 59, 999999)

        data = session.query(PortfolioDatasInstallmentsMapped, PortfolioDatasMapped). \
            join(PortfolioDatasMapped,
                 and_(
                     PortfolioDatasMapped.id == PortfolioDatasInstallmentsMapped.id_port_datas,
                     PortfolioDatasMapped.id_user == idUser
                 )
                 ). \
            filter(
            or_(
                and_(
                    PortfolioDatasMapped.is_recurring == True,
                    extract('year', PortfolioDatasMapped.created_at) <= year,
                    extract('month', PortfolioDatasMapped.created_at) <= int(monthStr[0])
                ),
                PortfolioDatasInstallmentsMapped.expiration_date.between(start_date, end_date)
            ),
            or_(
                PortfolioDatasInstallmentsMapped.is_paid == True,
                and_(
                    PortfolioDatasInstallmentsMapped.is_paid == None,
                    PortfolioDatasMapped.tag == TagDatasPortfolio.Receitas
                )
            ),
            PortfolioDatasInstallmentsMapped.id_user == idUser
        ). \
            all()

        unified_list = []

        for port_installment, port_data in data:
            unified_datas = UnifiedSomePortfolioData(
                value_installment=port_installment.value_installment,
                value=port_data.value,
                tag=port_data.tag,
                is_recurring=port_installment.is_recurring
            )
            unified_list.append(unified_datas)

        for data in unified_list:
            if data.tag == TagDatasPortfolio.Receitas:
                total_revenues += data.value_installment
            elif data.tag == TagDatasPortfolio.Receitas and data.is_recurring is True:
                total_revenues += data.value
            elif data.tag == TagDatasPortfolio.Despesas:
                total_expenses += data.value_installment

        return total_revenues - total_expenses
