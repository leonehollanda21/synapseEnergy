from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.unidadeConsumidora.models import UnidadeConsumidoraModel
from app.modules.unidadeConsumidora.schemas import UnidadeCreate
from app.modules.usuario.models import UsuarioModel


class UnidadeService:

    def criar_unidade(self, db: Session, unidade: UnidadeCreate, gestor: UsuarioModel):
        """
        Lógica de Negócio:
        1. Verifica se o Gestor pertence à mesma empresa informada na Unidade.
        2. Verifica unicidade do Código CCEE.
        """

        # Validação de Segurança: O gestor só pode criar unidades para a sua própria empresa
        print("aaa",gestor)
        if gestor.empresa_id != unidade.empresa_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operação negada: Você só pode cadastrar unidades para a sua própria empresa."
            )

        # Validação de Dados: Unicidade do CCEE
        existe = db.query(UnidadeConsumidoraModel).filter(
            UnidadeConsumidoraModel.codigo_ccee == unidade.codigo_ccee
        ).first()

        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código CCEE já cadastrado no sistema."
            )

        # Persistência
        nova_unidade = UnidadeConsumidoraModel(**unidade.dict())
        db.add(nova_unidade)
        db.commit()
        db.refresh(nova_unidade)
        return nova_unidade

    def listar_unidades_por_empresa(self, db: Session, empresa_id: int):
        return db.query(UnidadeConsumidoraModel).filter(
            UnidadeConsumidoraModel.empresa_id == empresa_id
        ).all()