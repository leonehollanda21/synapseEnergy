from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.contrato.schemas import ContratoCUSDCreate, ContratoACLCreate, ContratoResponse, ContratoVolumeCreate
from app.modules.contrato.repository import ContratoRepository
from app.modules.contrato.service import ContratoService


# Nota: Em um cenário ideal, teríamos um ContratoService aqui também
router = APIRouter(prefix="/contratos", tags=["Contratos (RF1.2)"])
repository = ContratoRepository()
service = ContratoService()


@router.post("/cusd", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato_distribuicao(contrato: ContratoCUSDCreate, db: Session = Depends(get_db)):
    """Cria um contrato de distribuição (CUSD) com a Enel."""
    return repository.create_cusd(db, contrato)

@router.post("/acl", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato_mercado_livre(contrato: ContratoACLCreate, db: Session = Depends(get_db)):
    """Cria um contrato de compra de energia (ACL)."""
    return repository.create_acl(db, contrato)

@router.post("/{contrato_id}/upload", status_code=status.HTTP_201_CREATED)
def upload_contrato_pdf(contrato_id: int, arquivo: UploadFile = File(...), db: Session = Depends(get_db)):
    """RF1.4: Faz upload do PDF do contrato."""
    return service.upload_pdf(db, contrato_id, arquivo)

@router.post("/{contrato_id}/volumes", status_code=status.HTTP_201_CREATED)
def adicionar_volumes_mensais(contrato_id: int, volumes: List[ContratoVolumeCreate], db: Session = Depends(get_db)):
    """RF1.3: Adiciona a sazonalização (volumes mensais)."""
    return service.adicionar_volumes(db, contrato_id, volumes)