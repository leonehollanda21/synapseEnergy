from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base
from app.modules.contrato.models import ContratoModel


class ContratoCUSDModel(ContratoModel):
    __tablename__ = "contratos_cusd"

    # Chave primária é FK da tabela pai
    id = Column(Integer, ForeignKey("contratos.id"), primary_key=True)

    demanda_ponta_kw = Column(Float, nullable=False)
    demanda_fora_ponta_kw = Column(Float, nullable=False)
    subgrupo_tarifario = Column(String)  # Ex: A4, A3

    __mapper_args__ = {
        'polymorphic_identity': 'cusd',
    }