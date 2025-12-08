from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.configuration.database import Base


class MedicaoModel(Base):
    __tablename__ = "medicoes"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    consumo_ponta_kwh = Column(Float)
    consumo_fora_ponta_kwh = Column(Float)
    demanda_medida_kw = Column(Float)

    unidade_id = Column(Integer, ForeignKey("unidades_consumidoras.id"))
    unidade = relationship("UnidadeConsumidoraModel", back_populates="medicoes")
