from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.configuration.database import Base
from app.models.contrato.contratoModel import ContratoModel


class ContratoACLModel(ContratoModel):
    __tablename__ = "contratos_acl"

    id = Column(Integer, ForeignKey("contratos.id"), primary_key=True)

    volume_mensal_mwh = Column(Float, nullable=False)
    preco_mwh = Column(Float, nullable=False)
    flexibilidade_min = Column(Float)
    flexibilidade_max = Column(Float)
    fonte_energia = Column(String)  # Ex: Incentivada 50%

    __mapper_args__ = {
        'polymorphic_identity': 'acl',
    }
