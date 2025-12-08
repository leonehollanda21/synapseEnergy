from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.configuration.database import Base
from app.models.pedidoCotacao.statusRFQEnum import StatusRFQEnum


class PedidoCotacaoModel(Base):
    __tablename__ = "pedidos_cotacao"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    data_inicio_suprimento = Column(Date)
    volume_desejado = Column(Float)
    prazo_resposta = Column(Date)
    status = Column(SAEnum(StatusRFQEnum), default=StatusRFQEnum.ABERTA)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relacionamentos
    usuario_criador = relationship("UsuarioModel", back_populates="rfqs_criadas")
    propostas = relationship("PropostaModel", back_populates="pedido_cotacao")
    simulacoes = relationship("SimulacaoModel", back_populates="pedido_cotacao")
