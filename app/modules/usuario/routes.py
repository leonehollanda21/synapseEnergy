from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.usuario.schemas import UsuarioCreate, UsuarioResponse
from app.modules.usuario.service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Perfis e Permissões (Módulo 4)"])
service = UsuarioService()

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return service.cadastrar_usuario(db, usuario)