from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.modules.usuario.repository import UsuarioRepository
from app.modules.usuario.schemas import UsuarioCreate, LoginRequest


class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def cadastrar_usuario(self, db: Session, usuario: UsuarioCreate):
        """
        Regra de Negócio:
        1. Verificar se o e-mail já existe.
        2. (Futuro) Gerar hash da senha.
        3. Persistir no banco.
        """
        db_usuario = self.repository.get_by_email(db, usuario.email)
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

        # Aqui no futuro você adicionará a lógica de:
        # usuario.senha = hash_password(usuario.senha)

        return self.repository.create(db, usuario)

    def buscar_por_email(self, db: Session, email: str):
        usuario = self.repository.get_by_email(db, email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return usuario

    def autenticar_usuario(self, db: Session, login: LoginRequest):
        # 1. Busca o usuário pelo e-mail
        usuario = self.repository.get_by_email(db, login.email)

        # 2. Verifica se existe e se a senha bate
        if not usuario or not verify_password(login.senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Gera o Token JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"id":usuario.id,"sub": usuario.email, "perfil": usuario.perfil},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "perfil": usuario.perfil,
            "nome": usuario.nome
        }