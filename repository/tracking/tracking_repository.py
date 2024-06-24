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
        data_revenues = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Receitas,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        data_expenses = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Despesas,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        data_investiment = session.query(PortfolioDatasMapped).filter(
            and_(
                PortfolioDatasMapped.tag == TagDatasPortfolio.Investimentos,
                PortfolioDatasMapped.id_user == idUser
            )
        ).all()

        type_profile_user = session.query(UserMapped).filter(UserMapped.id == idUser).one_or_none()

        totals_investiment = Decimal(sum(data.value for data in data_investiment))

        totals_revenues = Decimal(sum(data.value for data in data_revenues))

        totals_expenses = Decimal(sum(data.value for data in data_expenses))

        profiles = [Devedor(totals_revenues, totals_expenses, totals_investiment),
                    Intermediario(totals_revenues, totals_expenses, totals_investiment),
                    Investidor(totals_revenues, totals_expenses, totals_investiment)]

        profile_mappings = {
            Devedor: TypeProfileEnumDTO.Devedor,
            Intermediario: TypeProfileEnumDTO.Intermediario,
            Investidor: TypeProfileEnumDTO.Investidor
        }

        current_profile = type_profile_user.type_profile
        new_profile = current_profile

        for profile in profiles:
            if profile.check_profile():
                new_profile = profile_mappings[type(profile)]
                if new_profile != current_profile:
                    break

        change_profile = new_profile != current_profile

        tracking = calculateTrackingPercentages(totals_revenues, totals_expenses, totals_investiment, new_profile)

        response_body = {
            "change_profile": change_profile,
            "profile": new_profile,
            "tracking": tracking
        }

        if change_profile:
            user_type_profile = UserUpdateTypeProfile(type_profile=new_profile)
            updateTypeProfile(idUser, user_type_profile)

        return response_body


def calculateTrackingPercentages(totalsRevenues, totalsExpenses, totalsInvestiment, currentProfile):
    tracking = {
        "total_porcent": 0,
        "porcent": []
    }

    if currentProfile == TypeProfileEnumDTO.Devedor:
        next_profile = TypeProfileEnumDTO.Intermediario

        goal_1 = Decimal('0.2') * totalsExpenses
        goal_2 = Decimal('0.4') * totalsRevenues
        goal_3 = Decimal('0.2') * totalsRevenues
        goal_4 = totalsExpenses

        reached_goal_1 = min(totalsRevenues / goal_1, Decimal('1.0')) * 100 if totalsExpenses > 0 else 0
        reached_goal_2 = min(goal_2 / totalsExpenses, Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_3 = min(totalsInvestiment / goal_3, Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_4 = 100 if totalsRevenues >= goal_4 else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Receitas maior ou igual a 20% das despesas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Despesas menor que 40% das receitas",
            "porcent": int(reached_goal_2)
        })

        tracking["porcent"].append({
            "id": 3,
            "title": "Investimento maior que 20% das receitas",
            "porcent": int(reached_goal_3)
        })

        tracking["porcent"].append({
            "id": 4,
            "title": "Receitas maior ou igual a despesas",
            "porcent": int(reached_goal_4)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2 + reached_goal_3 + reached_goal_4) / 4)

    elif currentProfile == TypeProfileEnumDTO.Intermediario:
        next_profile = TypeProfileEnumDTO.Investidor

        goal_1 = Decimal('0.6') * totalsRevenues
        goal_2 = Decimal('0.7') * totalsExpenses
        goal_3 = totalsExpenses

        reached_goal_1 = min(totalsInvestiment / goal_1, Decimal('1.0')) * 100 if totalsRevenues > 0 else 0
        reached_goal_2 = min(totalsRevenues / goal_2, Decimal('1.0')) * 100 if totalsExpenses > 0 else 0
        reached_goal_3 = 100 if totalsRevenues > goal_3 else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Investimento maior ou igual a 60% das receitas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Receitas maior que 70% das despesas",
            "porcent": int(reached_goal_2)
        })

        tracking["porcent"].append({
            "id": 3,
            "title": "Receitas maior que as despesas",
            "porcent": int(reached_goal_3)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2 + reached_goal_3) / 3)

    elif currentProfile == TypeProfileEnumDTO.Investidor:
        tracking["porcent"].append({
            "id": 1,
            "title": "Você já atingiu o perfil mais alto",
            "porcent": 100
        })

        tracking["total_porcent"] = 100

    return tracking


