from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class DocumentoModel(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_arquivo = Column(String, nullable=False)
    caminho_url = Column(String, nullable=False)
    data_upload = Column(Date)

    contrato_id = Column(Integer, ForeignKey("contratos.id"))
    contrato = relationship("ContratoModel", back_populates="documentos")
