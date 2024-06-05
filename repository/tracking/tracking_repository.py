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

        tracking = calculateTrackingPercentages(totalsRevenues, totalsExpenses, totalsInvestiment, new_profile)

        response_body = {
            "change_profile": change_profile,
            "profile": new_profile,
            "tracking": tracking
        }

        if change_profile:
            user_type_profile = UserUpdateTypeProfile(type_profile=new_profile)
            updateTypeProfile(idUser, user_type_profile)

        return response_body


def calculateTrackingPercentages(totalsRevenues, totalsExpenses, totalsInvestiment, userProfile):
    tracking = {
        "total_porcent": 0,
        "porcent": []
    }

    if userProfile == TypeProfileEnumDTO.Devedor:
        revenue_expense_difference = Decimal(totalsRevenues) - Decimal(totalsExpenses)
        half_revenues = Decimal('0.5') * totalsRevenues

        reached_goal_1 = min(revenue_expense_difference / half_revenues, Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_2 = min(totalsInvestiment / (Decimal('0.05') * totalsRevenues), Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_3 = 100 if totalsExpenses > totalsRevenues else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Receitas - Despesas >= 50% das receitas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Investimento < 5% das receitas",
            "porcent": int(reached_goal_2)
        })

        tracking["porcent"].append({
            "id": 3,
            "title": "Despesas > Receitas",
            "porcent": int(reached_goal_3)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2 + reached_goal_3) / 3)

    elif userProfile == TypeProfileEnumDTO.Intermediario:
        twenty_percent_expenses = Decimal('0.2') * totalsExpenses
        forty_percent_revenues = Decimal('0.4') * totalsRevenues

        reached_goal_1 = min(totalsRevenues / twenty_percent_expenses, Decimal('1.0')) * 100 if totalsExpenses > 0 else 0
        reached_goal_2 = min(totalsExpenses / forty_percent_revenues, Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_3 = min(totalsInvestiment / (Decimal('0.2') * totalsRevenues), Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_4 = 100 if totalsRevenues >= totalsExpenses else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Receitas >= 20% das despesas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Despesas < 40% das receitas",
            "porcent": int(reached_goal_2)
        })

        tracking["porcent"].append({
            "id": 3,
            "title": "Investimento > 20% das receitas",
            "porcent": int(reached_goal_3)
        })

        tracking["porcent"].append({
            "id": 4,
            "title": "Receitas >= Despesas",
            "porcent": int(reached_goal_4)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2 + reached_goal_3 + reached_goal_4) / 4)

    elif userProfile == TypeProfileEnumDTO.Investidor:
        thirty_percent_revenues = Decimal('0.3') * totalsRevenues

        reached_goal_1 = min(totalsInvestiment / thirty_percent_revenues, Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_2 = 100 if totalsRevenues > Decimal('0.5') * totalsExpenses else 0
        reached_goal_3 = 100 if totalsRevenues > totalsExpenses else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Investimento >= 30% das receitas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Receitas > 50% das despesas",
            "porcent": int(reached_goal_2)
        })

        tracking["porcent"].append({
            "id": 3,
            "title": "Receitas > Despesas",
            "porcent": int(reached_goal_3)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2 + reached_goal_3) / 3)

    return tracking

