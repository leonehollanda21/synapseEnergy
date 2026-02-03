from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class SimulacaoModel(Base):
    __tablename__ = "simulacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome_cenario = Column(String, nullable=False)  # +string nomeCenario
    data_criacao = Column(DateTime, default=datetime.utcnow)  # +date dataCriacao

    # Campos financeiros do Diagrama UML
    economia_projetada = Column(Float)  # +float economiaProjetada
    custo_total_projetado = Column(Float)  # +float custoTotalProjetado

    # O campo JSON salva o "estado" da simulação (preços e volumes usados)
    # Equivalente ao +json parametrosUtilizados do seu diagrama
    parametros_json = Column(JSON)

    # Relacionamento: Uma simulação é baseada em um Pedido de Cotação (RFQ)
    # Conforme a linha "base_para" do seu diagrama
    pedido_cotacao_id = Column(Integer, ForeignKey("pedidos_cotacao.id"), nullable=True)
    pedido_cotacao = relationship("PedidoCotacaoModel", back_populates="simulacoes")

    # Vínculo com Usuário e Unidade (Essencial para as travas de segurança que fizemos)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades_consumidoras.id"), nullable=False)