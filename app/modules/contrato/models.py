from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.modules.contrato.enums import StatusContratoEnum


class ContratoModel(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    data_assinatura = Column(Date)
    status = Column(SAEnum(StatusContratoEnum), default=StatusContratoEnum.RASCUNHO)

    # Discriminador para herança (SQLAlchemy sabe qual filho é qual por aqui)
    tipo_contrato = Column(String)

    unidade_id = Column(Integer, ForeignKey("unidades_consumidoras.id"))
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))

    # Relacionamentos
    unidade = relationship("UnidadeConsumidoraModel", back_populates="contratos")
    fornecedor = relationship("FornecedorModel", back_populates="contratos")
    documentos = relationship("DocumentoModel", back_populates="contrato")
    alertas = relationship("AlertaModel", back_populates="contrato")

    # Configuração de Polimorfismo
    __mapper_args__ = {
        'polymorphic_identity': 'contrato',
        'polymorphic_on': tipo_contrato
    }