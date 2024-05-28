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

        current_profile = typeProfileUser.type_profile
        new_profile = current_profile

        for profile in profiles:
            if profile.check_profile():
                new_profile = profile_mappings[type(profile)]
                if new_profile != current_profile:
                    break

        change_profile = new_profile != current_profile

        tracking = calculateTrackingPercentages(totalsRevenues, totalsExpenses, totalsInvestiment)

        response_body = {
            "change_profile": change_profile,
            "profile": new_profile,
            "tracking": tracking
        }

        if change_profile:
            user_type_profile = UserUpdateTypeProfile(type_profile=new_profile)
            updateTypeProfile(idUser, user_type_profile)

        return response_body


def calculateTrackingPercentages(totalsRevenues, totalsExpenses, totalsInvestiment):
    tracking = {
        "total_porcent": 0,
        "porcent": []
    }

    half_expenses = Decimal('0.5') * totalsExpenses
    if totalsExpenses > 0:
        reached_goal_1 = min(totalsRevenues / half_expenses, Decimal('1.0')) * 100
    else:
        reached_goal_1 = 100

    thirty_percent_revenues = Decimal('0.3') * totalsRevenues
    if totalsRevenues > 0:
        reached_goal_2 = min(totalsInvestiment / thirty_percent_revenues, Decimal('1.0')) * 100
    else:
        reached_goal_2 = 0

    tracking["porcent"].append({
        "id": 1,
        "title": "50% da receita sobre as despesas",
        "porcent": int(reached_goal_1)
    })

    tracking["porcent"].append({
        "id": 2,
        "title": "30% de sua receita investida",
        "porcent": int(reached_goal_2)
    })

    tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2) / 2)

    return tracking
