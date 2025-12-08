from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.configuration.database import Base

class UnidadeConsumidoraModel(Base):
    __tablename__ = "unidades_consumidoras"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    codigo_ccee = Column(String, unique=True, nullable=False)
    endereco = Column(String)
    tensao_fornecimento = Column(Float) # em kV

    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    # Relacionamentos
    empresa = relationship("EmpresaModel", back_populates="unidades")
    medicoes = relationship("MedicaoModel", back_populates="unidade")
    contratos = relationship("ContratoModel", back_populates="unidade")
