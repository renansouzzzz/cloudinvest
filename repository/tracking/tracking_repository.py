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
            "title": "Investimento >= 60% das receitas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Receitas > 70% das despesas",
            "porcent": int(reached_goal_2)
        })

        tracking["porcent"].append({
            "id": 3,
            "title": "Receitas > Despesas",
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


