from sqlalchemy.orm import Session
from app.modules.usuario.models import UsuarioModel
from app.modules.usuario.schemas import UsuarioCreate

class UsuarioRepository:
    def create(self, db: Session, usuario: UsuarioCreate):
        db_usuario = UsuarioModel(
            nome=usuario.nome,
            email=usuario.email,
            senha_hash=usuario.senha, # No futuro, aqui entrará o hash
            perfil=usuario.perfil
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def get_by_email(self, db: Session, email: str):
        return db.query(UsuarioModel).filter(UsuarioModel.email == email).first()