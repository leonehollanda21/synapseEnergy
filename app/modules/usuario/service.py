from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.usuario.repository import UsuarioRepository
from app.modules.usuario.schemas import UsuarioCreate


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