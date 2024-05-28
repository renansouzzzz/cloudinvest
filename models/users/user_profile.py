from decimal import Decimal


class UserProfile:
    def __init__(self, totals_revenues, totals_expenses, totals_investment):
        self.totals_revenues = totals_revenues
        self.totals_expenses = totals_expenses
        self.totals_investment = totals_investment

    def check_profile(self):
        pass


class Devedor(UserProfile):
    def check_profile(self):
        if self.totals_investment == 0:
            return Decimal(self.totals_revenues) - Decimal(self.totals_expenses) >= Decimal('0.5') * Decimal(self.totals_revenues)
        return Decimal(self.totals_revenues) - Decimal(self.totals_expenses) >= Decimal('0.5') * Decimal(self.totals_revenues) and Decimal(self.totals_investment) < Decimal('0.2') * self.totals_revenues


class Intermediario(UserProfile):
    def check_profile(self):
        if self.totals_investment == 0:
            return Decimal(self.totals_revenues) >= Decimal('0.5') * Decimal(self.totals_expenses)
        return Decimal(self.totals_revenues) >= Decimal('0.5') * Decimal(self.totals_expenses) and Decimal(self.totals_investment) < Decimal('0.3') * Decimal(self.totals_revenues)


class Investidor(UserProfile):
    def check_profile(self):
        return Decimal(self.totals_investment) >= Decimal('0.3') * Decimal(self.totals_revenues) and Decimal(self.totals_revenues) > Decimal('0.5') * Decimal(self.totals_expenses)
