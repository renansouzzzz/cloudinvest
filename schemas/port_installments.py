from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Boolean
from config.database import Base
from sqlalchemy.orm import relationship


class PortfolioDatasInstallmentsSchema(Base):
    __tablename__ = 'port_installments'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id', onupdate='CASCADE'), nullable=False)
    id_port_datas = Column(Integer, ForeignKey('port_datas.id', onupdate='CASCADE'), nullable=False)
    current_installment = Column(Integer, nullable=True)
    value_installment = Column(Numeric(18, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    expiration_date = Column(DateTime, nullable=True)
    is_recurring = Column(Boolean, nullable=False, default=False)

    user = relationship('UserSchema')

    port_datas = relationship('PortfolioDatasSchema')


class PortfolioDatasInstallmentsMapped(PortfolioDatasInstallmentsSchema):
    pass
