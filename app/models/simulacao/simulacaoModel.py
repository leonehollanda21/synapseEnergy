from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.configuration.database import Base

class SimulacaoModel(Base):
    __tablename__ = "simulacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome_cenario = Column(String, nullable=False)
    data_criacao = Column(Date)
    economia_projetada = Column(Float)
    parametros_json = Column(JSON) # Salva os parametros usados na simulação

    pedido_cotacao_id = Column(Integer, ForeignKey("pedidos_cotacao.id"))
    pedido_cotacao = relationship("PedidoCotacaoModel", back_populates="simulacoes")