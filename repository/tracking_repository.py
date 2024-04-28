from sqlalchemy import and_
from sqlalchemy.orm import Session

from config.database import engine
from models.portfolio_datas import TagDatasPortfolio
from models.user import TypeProfileEnumDTO, UserUpdateTypeProfile
from repository.user_repository import updateTypeProfile
from schemas.portfolio_datas import PortfolioDatasMapped


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

        totals = sum(
            data.value for data in dataRevenues
        ) - sum(
            data.value for data in dataExpenses
        )

        if totals > totalsRevenues and totals > 0.5 * totalsRevenues:
            userTypeProfile = UserUpdateTypeProfile.type_profile = TypeProfileEnumDTO.Devedor.value
            updateTypeProfile(idUser, userTypeProfile)

        if totalsRevenues < totals < 0.5 * totalsRevenues:
            userTypeProfile = UserUpdateTypeProfile.type_profile = TypeProfileEnumDTO.Intermediario.value
            updateTypeProfile(idUser, userTypeProfile)

        if totalsRevenues > totals and totalsRevenues > 0.3 * totalsInvestement:
            userTypeProfile = UserUpdateTypeProfile.type_profile = TypeProfileEnumDTO.Investidor.value
            updateTypeProfile(idUser, userTypeProfile)

        return True


