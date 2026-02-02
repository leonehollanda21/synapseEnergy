from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.empresa.schemas import CadastroEmpresaConsumidoraRequest, EmpresaResponse
from app.modules.empresa.service import EmpresaService

router = APIRouter(prefix="/empresas", tags=["Empresas"])
service = EmpresaService()

@router.post("/consumidora", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_empresa_consumidora(
    dados_cadastro: CadastroEmpresaConsumidoraRequest,
    db: Session = Depends(get_db)
):
    return service.cadastrar_empresa_consumidora(db, dados_cadastro)