from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class ContratoVolumeModel(Base):
    __tablename__ = "contratos_volumes"

    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("contratos.id")) # Vinculado à tabela pai ou ACL
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    volume_mwh = Column(Float, nullable=False)
    preco_mwh = Column(Float, nullable=False)

    contrato = relationship("ContratoModel", back_populates="volumes_mensais")