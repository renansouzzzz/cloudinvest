from sqlalchemy import and_
from sqlalchemy.orm import Session


from config.database import engine
from models.portfolio_datas import TagDatasPortfolio
from models.user import TypeProfileEnumDTO, UserUpdateTypeProfile
from repository.user_repository import updateTypeProfile
from schemas.portfolio_datas import PortfolioDatasMapped
from decimal import Decimal


def updateProfileByTracking(idUser: int):
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

        dataInvestiment = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Investimentos,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        totalsInvestement = sum(data.value for data in dataInvestiment)

        totalsRevenues = sum(data.value for data in dataRevenues)

        totalsExpenses = sum(data.value for data in dataExpenses)

        if totalsExpenses - totalsRevenues == Decimal('0.5') * totalsRevenues:
            userTypeProfile = UserUpdateTypeProfile(type_profile=TypeProfileEnumDTO.Devedor)
            updateTypeProfile(idUser, userTypeProfile)
        elif totalsRevenues > Decimal('1.5') * totalsExpenses:
            userTypeProfile = UserUpdateTypeProfile(type_profile=TypeProfileEnumDTO.Intermediario)
            updateTypeProfile(idUser, userTypeProfile)
        elif totalsInvestement > Decimal('0.3') * totalsRevenues:
            userTypeProfile = UserUpdateTypeProfile(type_profile=TypeProfileEnumDTO.Investidor)
            updateTypeProfile(idUser, userTypeProfile)

        return True

