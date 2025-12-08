from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.configuration.database import Base

class PropostaModel(Base):
    __tablename__ = "propostas"

    id = Column(Integer, primary_key=True, index=True)
    preco_ofertado_mwh = Column(Float, nullable=False)
    condicoes_pagamento = Column(Text)
    validade_proposta = Column(Date)
    status = Column(String) # Enviada, Aceita

    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    pedido_cotacao_id = Column(Integer, ForeignKey("pedidos_cotacao.id"))

    # Relacionamentos
    fornecedor = relationship("FornecedorModel", back_populates="propostas")
    pedido_cotacao = relationship("PedidoCotacaoModel", back_populates="propostas")
