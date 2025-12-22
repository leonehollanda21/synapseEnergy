from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
import shutil
import os
from datetime import date
from typing import List

from app.modules.contrato.repository import ContratoRepository
from app.modules.contrato.schemas import ContratoVolumeCreate

UPLOAD_DIR = "uploads/contratos"


class ContratoService:
    def __init__(self):
        self.repository = ContratoRepository()
        # Garante que a pasta existe ao iniciar o serviço
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def upload_pdf(self, db: Session, contrato_id: int, arquivo: UploadFile):
        # 1. Validação: Contrato existe?
        contrato = self.repository.get_by_id(db, contrato_id)
        if not contrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato não encontrado"
            )

        # 2. Define caminho físico
        caminho_arquivo = f"{UPLOAD_DIR}/{contrato_id}_{arquivo.filename}"

        # 3. Lógica de Arquivo (IO)
        try:
            with open(caminho_arquivo, "wb") as buffer:
                shutil.copyfileobj(arquivo.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar arquivo: {str(e)}"
            )

        # 4. Chama repositório para salvar metadados
        return self.repository.create_documento(
            db=db,
            nome_arquivo=arquivo.filename,
            caminho=caminho_arquivo,
            data_upload=date.today(),
            contrato_id=contrato_id
        )

    def adicionar_volumes(self, db: Session, contrato_id: int, volumes: List[ContratoVolumeCreate]):
        # 1. Validação
        contrato = self.repository.get_by_id(db, contrato_id)
        if not contrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato não encontrado"
            )

        # 2. Chama repositório
        qtd_adicionada = self.repository.create_volumes_mensais(db, contrato_id, volumes)
        return {"message": f"{qtd_adicionada} registros de volume adicionados."}