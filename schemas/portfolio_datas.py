from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, ForeignKey, String, Enum, DateTime
from config.database import Base
from sqlalchemy.orm import relationship
from models.portfolio_datas import TagDatasPortfolio


class PortfolioDatasSchema(Base):
    __tablename__ = 'port_datas'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id', onupdate='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    tag: TagDatasPortfolio = Column(Enum(TagDatasPortfolio))
    installment = Column(Integer, nullable=True)
    value = Column(Numeric(18, 2), nullable=False)
    expiration_day = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship('UserSchema')


class PortfolioDatasMapped(PortfolioDatasSchema):
    pass
