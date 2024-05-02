from sqlalchemy import and_
from sqlalchemy.orm import Session

from config.database import engine
from models.portfolio_datas import TagDatasPortfolio
from models.user import UserUpdateTypeProfile, TypeProfileEnumDTO
from models.user_profile import Devedor, Intermediario, Investidor
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

        totalsExpenses = sum(data.value for data in dataExpenses)

        profiles = [Devedor(totalsRevenues, totalsExpenses, totalsInvestement),
                    Intermediario(totalsRevenues, totalsExpenses, totalsInvestement),
                    Investidor(totalsRevenues, totalsExpenses, totalsInvestement)]

        profile_mappings = {
            Devedor: TypeProfileEnumDTO.Devedor,
            Intermediario: TypeProfileEnumDTO.Intermediario,
            Investidor: TypeProfileEnumDTO.Investidor
        }

        for profile in profiles:
            if profile.check_profile():
                user_type_profile = UserUpdateTypeProfile(type_profile=profile_mappings[type(profile)])
                updateTypeProfile(idUser, user_type_profile)

        return True

