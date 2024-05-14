import datetime

from MySQLdb import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from config.db.database import engine
from models.portfolio.portfolio_datas import PortfolioDatasUpdate, TagDatasPortfolio
from schemas.portfolio.port_installments import PortfolioDatasInstallmentsMapped
from schemas.portfolio.portfolio_datas import PortfolioDatasMapped
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

        start_date = datetime.datetime(year, int(monthStr[0]), 1, 0, 0, 0, 0)
        end_date = datetime.datetime(year, int(monthStr[0]), int(monthStr[1]), 23, 59, 59, 9999)

        data = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.id_user == idUser,
                PortfolioDatasMapped.created_at.between(start_date, end_date)
            )
        ).all()

        if data is None:
            raise ValueError(f'Nenhum dado foi encontrado!')
        return data


def calculatePortfolioBalance(idUser: int):
    with Session(engine) as session:
        dataRevenues = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Receitas,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        dataExpenses = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Despesas,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        if not dataRevenues and not dataExpenses:
            raise ValueError(f'Nenhum dado foi encontrado!')

        return sum(data.value for data in dataRevenues) - sum(data.value for data in dataExpenses)


def calculatePortfolioRevenuesTotals(idUser: int):
    with Session(engine) as session:
        dataRevenues = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Receitas,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        if not dataRevenues:
            raise ValueError(f'Nenhum dado foi encontrado!')

        return sum(data.value for data in dataRevenues)


def calculatePortfolioExpensesTotals(idUser: int):
    with Session(engine) as session:
        dataExpenses = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Despesas,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        if not dataExpenses:
            raise ValueError(f'Nenhum dado foi encontrado!')
        return 0 - sum(data.value for data in dataExpenses)


def calculatePortfolioInvestimentTotals(idUser: int):
    with Session(engine) as session:
        dataInvestiment = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Investimentos,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        if not dataInvestiment:
            raise ValueError(f'Nenhum dado foi encontrado!')
        return sum(data.value for data in dataInvestiment)


def getById(id: int):
    with Session(engine) as session:
        data = session.get(PortfolioDatasMapped, id)

        if not data:
            raise ValueError(f'O usuário com ID {id} não foi encontrado!')

        return data


def create(payload: PortfolioDatasMapped):
    with Session(engine) as session:
        try:
            portfolio_datas = PortfolioDatasMapped(**payload.dict())
        
            session.add(portfolio_datas)
            session.commit()
            session.refresh(portfolio_datas)

            if portfolio_datas.expiration_day is None and portfolio_datas.installment is None:
                installment = PortfolioDatasInstallmentsMapped(
                    id_user=portfolio_datas.id_user,
                    id_port_datas=portfolio_datas.id,
                    current_installment=None,
                    value_installment=portfolio_datas.value,
                    created_at=datetime.datetime.now(),
                    expiration_date=datetime.datetime.now(),
                    is_recurring=portfolio_datas.is_recurring,
                    is_paid=None
                )                   
                session.add(installment)
                session.commit()            
                return True

            installment_dates = []
            current_date = datetime.date(
                datetime.datetime.today().year, datetime.datetime.today().month - 1, portfolio_datas.expiration_day
            )

            today = datetime.datetime.now().date()

            for i in range(portfolio_datas.installment):
                days_in_month = ParseToTypes.parseMonthToDays(current_date.month)
                current_date += datetime.timedelta(days=days_in_month)
                if current_date < today:
                    current_date = datetime.date(
                        datetime.datetime.today().year, datetime.datetime.today().month + 1,
                        portfolio_datas.expiration_day
                    )
                installment_dates.append(current_date)

            installments = []
            for i, date in enumerate(installment_dates):
                installment = PortfolioDatasInstallmentsMapped(
                    id_user=portfolio_datas.id_user,
                    id_port_datas=portfolio_datas.id,
                    current_installment=i + 1,
                    value_installment=portfolio_datas.value / portfolio_datas.installment,
                    created_at=datetime.datetime.now(),
                    expiration_date=date,
                    is_recurring=portfolio_datas.is_recurring
                )
                installments.append(installment)

            session.bulk_save_objects(installments)
            session.commit()

        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Error on database: {e}")

        return True


def update(idPortDatas: int, payload: PortfolioDatasUpdate):
    with Session(engine) as session:
        try:
            get_port_datas = session.query(PortfolioDatasMapped).filter(
                PortfolioDatasMapped.id == idPortDatas
            ).one_or_none()

            for var, value in vars(payload).items():
                setattr(get_port_datas, var, value)

            session.add(get_port_datas)

            port_installments = session.query(PortfolioDatasInstallmentsMapped).filter(
                PortfolioDatasInstallmentsMapped.id_port_datas == get_port_datas.id
            ).all()

            for installment in port_installments:
                installment.value_installment = payload.value / payload.installment
                session.add(installment)

            session.commit()

        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error on database: {e}')

    return True


def delete(idPortDatas: int):
    with Session(engine) as session:
        try:
            getInstallments = session.query(PortfolioDatasInstallmentsMapped).filter(
                PortfolioDatasInstallmentsMapped.id_port_datas == idPortDatas
            ).all()

            if not getInstallments:
                raise HTTPException(status_code=404, detail="Informação não encontrada!")

            for installment in getInstallments:
                session.delete(installment)

            getPortfolioData = session.get(PortfolioDatasMapped, idPortDatas)

            if not getPortfolioData:
                raise HTTPException(status_code=404, detail="Informação não encontrada!")

            session.delete(getPortfolioData)
            session.commit()

        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f'Error on database: {e}')

        return "Informação deletada com sucesso!"
