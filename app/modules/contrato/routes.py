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
    """Novo Contrato de Distribuição (CUSD): Registra o contrato de "Fio" com a Enel. Aqui definimos a Demanda Contratada (Ponta e Fora Ponta), que é o limite de potência que a fábrica pode usar sem pagar multa."""
    return repository.create_cusd(db, contrato)

@router.post("/acl", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato_mercado_livre(contrato: ContratoACLCreate, db: Session = Depends(get_db)):
    """Novo Contrato de Energia (ACL): Registra a compra da energia propriamente dita no Mercado Livre. Definimos preço, volume médio e fonte (ex: Energia Incentivada)."""
    return repository.create_acl(db, contrato)

@router.post("/{contrato_id}/upload", status_code=status.HTTP_201_CREATED)
def upload_contrato_pdf(contrato_id: int, arquivo: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload de PDF do Contrato: Permite anexar o arquivo digital original (PDF) ao cadastro. O sistema salva o arquivo de forma segura no servidor e cria um link de referência no banco de dados."""
    return service.upload_pdf(db, contrato_id, arquivo)

@router.post("/{contrato_id}/volumes", status_code=status.HTTP_201_CREATED)
def adicionar_volumes_mensais(contrato_id: int, volumes: List[ContratoVolumeCreate], db: Session = Depends(get_db)):
    """Sazonalização (Volumes Mensais): Como a indústria não consome igual o ano todo, esta rota permite detalhar o volume contratado mês a mês (Ex: Jan=100, Fev=120), garantindo uma auditoria precisa."""
    return service.adicionar_volumes(db, contrato_id, volumes)