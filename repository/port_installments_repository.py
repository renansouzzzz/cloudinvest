from sqlalchemy.orm import Session

from config.database import engine
from schemas.port_installments import PortfolioDatasInstallmentsSchema


def getAll():
    with Session(engine) as session:
        data = session.query(PortfolioDatasInstallmentsSchema).all()
        if data is None:
            raise ValueError(f'Nenhum usuário foi encontrado!')
        return data
