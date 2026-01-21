from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.usuario.enums import PerfilEnum
from app.modules.usuario.models import UsuarioModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UsuarioModel:

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou ausentes",
            headers={"WWW-Authenticate": "Bearer"},
        )


    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="A decodificação de JWT e busca no banco ainda não foram implementadas."
    )


class RoleChecker:
    def __init__(self, allowed_roles: list[PerfilEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UsuarioModel = Depends(get_current_user)):
        if user.perfil not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para realizar esta operação."
            )
        return True


perm_analista = RoleChecker([PerfilEnum.ANALISTA, PerfilEnum.ADMIN])
perm_gestor = RoleChecker([PerfilEnum.GESTOR, PerfilEnum.ANALISTA, PerfilEnum.ADMIN])
perm_fornecedor = RoleChecker([PerfilEnum.FORNECEDOR])