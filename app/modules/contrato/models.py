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
    tipo_contrato = Column(String)

    unidade_id = Column(Integer, ForeignKey("unidades_consumidoras.id"))
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))

    # Relacionamentos
    # Usamos apenas o nome da classe como string para evitar erros de importação circular
    unidade = relationship("UnidadeConsumidoraModel", back_populates="contratos")
    fornecedor = relationship("FornecedorModel", back_populates="contratos")

    documentos = relationship("DocumentoModel", back_populates="contrato")
    volumes_mensais = relationship("ContratoVolumeModel", back_populates="contrato")

    # --- CORREÇÃO: Adicionando relacionamento reverso de Alertas ---
    alertas = relationship("AlertaModel", back_populates="contrato")

    __mapper_args__ = {
        'polymorphic_identity': 'contrato',
        'polymorphic_on': tipo_contrato
    }