from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class AlertaModel(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    mensagem = Column(String)
    lido = Column(Integer, default=0)
    tipo = Column(String)

    contrato_id = Column(Integer, ForeignKey("contratos.id"))
    contrato = relationship("ContratoModel", back_populates="alertas")
