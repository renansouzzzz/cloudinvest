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


def calculateTrackingPercentages(totals_revenues, totals_expenses, totals_investment, currentProfile):
    tracking = {
        "total_porcent": 0,
        "porcent": []
    }

    if currentProfile == TypeProfileEnumDTO.Devedor:

        reached_goal_1 = 100 if Decimal(totals_revenues) > Decimal(totals_expenses) else 0
        reached_goal_2 = 100 if Decimal(totals_investment) < Decimal('0.3') * Decimal(totals_revenues) else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Receitas maior que as despesas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Investimento menor que 30% das receitas",
            "porcent": int(reached_goal_2)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2) / 2)

    elif currentProfile == TypeProfileEnumDTO.Intermediario:

        reached_goal_1 = 100 if Decimal(totals_revenues) > Decimal(totals_expenses) else 0
        reached_goal_2 = 100 if Decimal(totals_investment) >= Decimal('0.3') * Decimal(totals_revenues) else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Receitas maior que as despesas",
            "porcent": int(reached_goal_1)
        })

        tracking["porcent"].append({
            "id": 2,
            "title": "Investimento maior ou igual a 30% das receitas",
            "porcent": int(reached_goal_2)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2) / 2)

    elif currentProfile == TypeProfileEnumDTO.Investidor:

        reached_goal_1 = 100 if Decimal(totals_revenues) > Decimal(totals_expenses) else 0
        reached_goal_2 = 100 if Decimal(totals_investment) >= Decimal('0.3') * Decimal(totals_revenues) else 0

        tracking["porcent"].append({
            "id": 1,
            "title": "Você atingiu o último perfil, parabéns!",
            "porcent": int(reached_goal_1)
        })

        tracking["total_porcent"] = int((reached_goal_1 + reached_goal_2) / 2)

    return tracking
