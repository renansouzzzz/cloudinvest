from decimal import Decimal

from sqlalchemy import and_
from sqlalchemy.orm import Session

from config.db.database import engine
from models.portfolio.portfolio_datas import TagDatasPortfolio
from models.users.user import UserUpdateTypeProfile, TypeProfileEnumDTO
from models.users.user_profile import Devedor, Intermediario, Investidor
from repository.users.user_repository import updateTypeProfile
from schemas.portfolio.portfolio_datas import PortfolioDatasMapped
from schemas.users.user import UserMapped


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

        typeProfileUser = session.query(UserMapped).filter(UserMapped.id == idUser).one_or_none()

        totalsInvestiment = Decimal(sum(data.value for data in dataInvestiment))

        totalsRevenues = Decimal(sum(data.value for data in dataRevenues))

        totalsExpenses = Decimal(sum(data.value for data in dataExpenses))

        profiles = [Devedor(totalsRevenues, totalsExpenses, totalsInvestiment),
                    Intermediario(totalsRevenues, totalsExpenses, totalsInvestiment),
                    Investidor(totalsRevenues, totalsExpenses, totalsInvestiment)]

        profile_mappings = {
            Devedor: TypeProfileEnumDTO.Devedor,
            Intermediario: TypeProfileEnumDTO.Intermediario,
            Investidor: TypeProfileEnumDTO.Investidor
        }

        for profile in profiles:
            if profile.check_profile():
                user_type_profile = UserUpdateTypeProfile(type_profile=profile_mappings[type(profile)])
                return updateTypeProfile(idUser, user_type_profile)
            else:
                update_return = (False, typeProfileUser.type_profile)

        return update_return

