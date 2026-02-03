from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import validar_gestor
from app.modules import UsuarioModel
from app.modules.unidadeConsumidora.service import UnidadeService
from app.modules.unidadeConsumidora.models import UnidadeConsumidoraModel
from app.modules.unidadeConsumidora.schemas import UnidadeCreate, UnidadeResponse

router = APIRouter(prefix="/unidades", tags=["Unidades Consumidoras (RF2.1)"])
service = UnidadeService()

@router.post("/", response_model=UnidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_unidade(
    unidade: UnidadeCreate,
    db: Session = Depends(get_db),
    gestor_atual: UsuarioModel = Depends(validar_gestor)
):
    return service.criar_unidade(db, unidade, gestor_atual)


@router.get("/", response_model=List[UnidadeResponse])
def listar_unidades(db: Session = Depends(get_db)):
    """Permite visualizar todas as filiais cadastradas para selecionar qual delas vamos monitorar."""
    return db.query(UnidadeConsumidoraModel).all()