class UnifiedAllPortfolioData:
    def __init__(self, idPortData, idUser, name, tag, installment, value, expiration_day, created_at,
                 current_installment, value_installment, expiration_date, is_recurring):
        self.idPortData = idPortData
        self.idUser = idUser
        self.name = name
        self.tag = tag
        self.installment = installment
        self.value = value
        self.expiration_day = expiration_day
        self.created_at = created_at
        self.current_installment = current_installment
        self.value_installment = value_installment
        self.expiration_date = expiration_date
        self.is_recurring = is_recurring
