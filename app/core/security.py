from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.usuario.enums import PerfilEnum
from app.modules.usuario.models import UsuarioModel

# Configuração para extrair o Token do Header "Authorization: Bearer <TOKEN>"
# O tokenUrl aponta para onde o Swagger deve enviar as credenciais para logar
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UsuarioModel:
    """
    Dependência para validar o Token JWT e retornar o usuário do banco de dados.
    A lógica de decodificação do JWT (SECRET_KEY, ALGORITHM) será inserida aqui em breve.
    """
    # Placeholder: Esta lógica será substituída pela decodificação real do JWT
    # Por enquanto, apenas definimos a assinatura da função para integração posterior
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou ausentes",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Futuramente: payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # Futuramente: user = db.query(UsuarioModel).filter(UsuarioModel.email == payload.get("sub")).first()

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="A decodificação de JWT e busca no banco ainda não foram implementadas."
    )


# Esta classe funciona como um "Guarda de Trânsito" para as rotas
class RoleChecker:
    def __init__(self, allowed_roles: list[PerfilEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UsuarioModel = Depends(get_current_user)):
        """
        Verifica se o perfil do usuário (obtido via token) está na lista de perfis permitidos.
        Agora a classe depende automaticamente de 'get_current_user'.
        """
        if user.perfil not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para realizar esta operação."
            )
        return True


# Definição de permissões comuns para facilitar o uso nas rotas
perm_analista = RoleChecker([PerfilEnum.ANALISTA, PerfilEnum.ADMIN])
perm_gestor = RoleChecker([PerfilEnum.GESTOR, PerfilEnum.ANALISTA, PerfilEnum.ADMIN])
perm_fornecedor = RoleChecker([PerfilEnum.FORNECEDOR])