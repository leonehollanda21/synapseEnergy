from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.unidadeConsumidora.models import UnidadeConsumidoraModel
from app.modules.unidadeConsumidora.schemas import UnidadeCreate, UnidadeResponse

router = APIRouter(prefix="/unidades", tags=["Unidades Consumidoras (RF2.1)"])


@router.post("/", response_model=UnidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_unidade(unidade: UnidadeCreate, db: Session = Depends(get_db)):
    """Aqui registramos o ponto físico de consumo, incluindo o código único da CCEE e a tensão de fornecimento. É a "identidade" da fábrica no setor elétrico."""
    existe = db.query(UnidadeConsumidoraModel).filter(
        UnidadeConsumidoraModel.codigo_ccee == unidade.codigo_ccee).first()
    if existe:
        raise HTTPException(status_code=400, detail="Código CCEE já cadastrado.")

    nova_unidade = UnidadeConsumidoraModel(**unidade.dict())
    db.add(nova_unidade)
    db.commit()
    db.refresh(nova_unidade)
    return nova_unidade


@router.get("/", response_model=List[UnidadeResponse])
def listar_unidades(db: Session = Depends(get_db)):
    """Permite visualizar todas as filiais cadastradas para selecionar qual delas vamos monitorar."""
    return db.query(UnidadeConsumidoraModel).all()