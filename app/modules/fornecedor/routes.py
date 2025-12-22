from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.modules.fornecedor.schemas import FornecedorCreate, FornecedorResponse
from app.modules.fornecedor.service import FornecedorService

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores (RF1.1)"])
service = FornecedorService()

@router.post("/", response_model=FornecedorResponse, status_code=status.HTTP_201_CREATED)
def criar_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    """Cadastra um novo fornecedor (Distribuidora ou Comercializadora)."""
    return service.criar_fornecedor(db, fornecedor)

@router.get("/", response_model=List[FornecedorResponse])
def listar_fornecedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os fornecedores cadastrados."""
    return service.listar_fornecedores(db, skip, limit)