from decimal import Decimal


class UserProfile:
    def __init__(self, totals_revenues, totals_expenses, totals_investment):
        self.totals_revenues = totals_revenues
        self.totals_expenses = totals_expenses
        self.totals_investment = totals_investment

    def check_profile(self):
        pass


class UserProfile:
    def __init__(self, totals_revenues, totals_expenses, totals_investment):
        self.totals_revenues = totals_revenues
        self.totals_expenses = totals_expenses
        self.totals_investment = totals_investment


class Devedor(UserProfile):
    def check_profile(self):
        return Decimal(self.totals_expenses) < Decimal(self.totals_revenues) and Decimal(self.totals_investment) < 0


class Intermediario(UserProfile):
    def check_profile(self):
        return Decimal(self.totals_revenues) > Decimal(self.totals_expenses) and Decimal(self.totals_investment) < Decimal('0.3') * Decimal(self.totals_investment)


class Investidor(UserProfile):
    def check_profile(self):
        return Decimal(self.totals_revenues) > Decimal(self.totals_expenses) and Decimal(self.totals_investment) >= Decimal('0.3') * Decimal(self.totals_revenues)
