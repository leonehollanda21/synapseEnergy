from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.configuration.database import Base
from app.models.fornecedor.tipoFornecedorEnum import TipoFornecedorEnum


class FornecedorModel(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    tipo = Column(SAEnum(TipoFornecedorEnum), nullable=False)
    contato_nome = Column(String)
    contato_email = Column(String)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    # Relacionamentos
    empresa = relationship("EmpresaModel", back_populates="fornecedores")
    contratos = relationship("ContratoModel", back_populates="fornecedor")
    propostas = relationship("PropostaModel", back_populates="fornecedor")
