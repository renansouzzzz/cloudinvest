from sqlalchemy import and_
from sqlalchemy.orm import Session

from config.database import engine
from schemas.port_installments import PortfolioDatasInstallmentsSchema, PortfolioDatasInstallmentsMapped
from schemas.portfolio_datas import PortfolioDatasMapped
from utils.parse_types import ParseToTypes


class UnifiedData:
    def __init__(self, idPortData, idUser, name, tag, installment, value, expiration_day, created_at,
                 current_installment, value_installment, expiration_date):
        self.idPortData = idPortData
        self.idUser = idUser
        self.name = name
        self.tag = tag
        self.installment = installment
        self.value = value
        self.expiration_day = expiration_day
        self.created_at = created_at
        self.current_installment = current_installment
        self.value_installment = value_installment
        self.expiration_date = expiration_date


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

        data = session.query(PortfolioDatasInstallmentsMapped, PortfolioDatasMapped). \
            join(PortfolioDatasMapped,
                 and_(PortfolioDatasMapped.id == PortfolioDatasInstallmentsMapped.id_port_datas,
                      PortfolioDatasMapped.id_user == idUser)). \
            filter(PortfolioDatasInstallmentsMapped.expiration_date.between(start_date, end_date),
                   PortfolioDatasInstallmentsMapped.id_user == idUser). \
            all()

        if data is None:
            raise ValueError('Nenhum dado foi encontrado!')

        unified_list = []

        for port_installment, port_data in data:
            unified_datas = UnifiedData(
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
                tag=port_data.tag
            )
            unified_list.append(unified_datas)

        return unified_list
