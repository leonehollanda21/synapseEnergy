from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.configuration.database import Base


class EmpresaModel(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    setor_atuacao = Column(String)

    usuarios = relationship("UsuarioModel", back_populates="empresa")
    unidades = relationship("UnidadeConsumidoraModel", back_populates="empresa")
    fornecedores = relationship("FornecedorModel", back_populates="empresa")
