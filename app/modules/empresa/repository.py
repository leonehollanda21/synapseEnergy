from sqlalchemy.orm import Session
from app.modules.empresa.models import EmpresaModel
from app.modules.empresa.schemas import EmpresaCreate

class EmpresaRepository:
    def get_by_cnpj(self, db: Session, cnpj: str):
        return db.query(EmpresaModel).filter(EmpresaModel.cnpj == cnpj).first()

    def create(self, db: Session, empresa: EmpresaCreate):
        db_empresa = EmpresaModel(
            razao_social=empresa.razao_social,
            cnpj=empresa.cnpj,
            setor_atuacao=empresa.setor_atuacao
        )
        db.add(db_empresa)
        db.flush()
        return db_empresa

