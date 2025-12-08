from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.configuration.database import Base
from app.models.usuario.perfilEnum import PerfilEnum


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(SAEnum(PerfilEnum), nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    # Relacionamentos
    empresa = relationship("EmpresaModel", back_populates="usuarios")
    rfqs_criadas = relationship("PedidoCotacaoModel", back_populates="usuario_criador")
