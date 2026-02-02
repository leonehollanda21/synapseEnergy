from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.empresa.repository import EmpresaRepository
from app.modules.empresa.schemas import CadastroEmpresaConsumidoraRequest
from app.modules.usuario.repository import UsuarioRepository
from app.modules.usuario.models import UsuarioModel
from app.modules.usuario.enums import PerfilEnum

# Importando a função que acabamos de criar
from app.core.security import get_password_hash


class EmpresaService:
    def __init__(self):
        self.empresa_repository = EmpresaRepository()
        self.usuario_repository = UsuarioRepository()

    def cadastrar_empresa_consumidora(self, db: Session, dados: CadastroEmpresaConsumidoraRequest):
        if self.usuario_repository.get_by_email(db, dados.gestor.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email do gestor já cadastrado"
            )

        if self.empresa_repository.get_by_cnpj(db, dados.empresa.cnpj):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já cadastrado"
            )

        try:
            nova_empresa = self.empresa_repository.create(db, dados.empresa)

            novo_usuario = UsuarioModel(
                nome=dados.gestor.nome,
                email=dados.gestor.email,
                senha_hash=get_password_hash(dados.gestor.senha),
                perfil=PerfilEnum.GESTOR,
                empresa_id=nova_empresa.id
            )

            db.add(novo_usuario)
            db.commit()

            db.refresh(nova_empresa)
            return nova_empresa

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao cadastrar empresa e gestor: {str(e)}"
            )