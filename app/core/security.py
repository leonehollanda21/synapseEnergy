import hashlib

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt # Precisará de: pip install "python-jose[cryptography]"
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from app.modules.usuario.enums import PerfilEnum
from app.modules.usuario.models import UsuarioModel


# Configurações do JWT (Em produção, use variáveis de ambiente)
SECRET_KEY = "sua_chave_secreta_super_segura_e_longa_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 horas


# Configuração para Hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Aplica o SHA-256 antes de verificar com o bcrypt para manter
    consistência com o cadastro (limite de 72 bytes).
    """
    senha_pre_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(senha_pre_hash, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
        auth: HTTPAuthorizationCredentials = Depends(security),  # Recebe as credenciais do Bearer
        db: Session = Depends(get_db)
) -> UsuarioModel:
    token = auth.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[PerfilEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UsuarioModel = Depends(get_current_user)):
        if user.perfil not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para realizar esta operação."
            )
        return user

validar_gestor = RoleChecker([PerfilEnum.GESTOR, PerfilEnum.ADMIN])

validar_analista = RoleChecker([PerfilEnum.ANALISTA, PerfilEnum.ADMIN])

validar_fornecedor = RoleChecker([PerfilEnum.FORNECEDOR])