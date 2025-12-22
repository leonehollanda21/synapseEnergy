from sqlalchemy.orm import Session
from app.modules.fornecedor.models import FornecedorModel
from app.modules.fornecedor.schemas import FornecedorCreate, FornecedorUpdate

class FornecedorRepository:
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(FornecedorModel).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, fornecedor_id: int):
        return db.query(FornecedorModel).filter(FornecedorModel.id == fornecedor_id).first()

    def get_by_cnpj(self, db: Session, cnpj: str):
        return db.query(FornecedorModel).filter(FornecedorModel.cnpj == cnpj).first()

    def create(self, db: Session, fornecedor: FornecedorCreate):
        # Transforma o Schema Pydantic em Model SQLAlchemy
        db_fornecedor = FornecedorModel(
            razao_social=fornecedor.razao_social,
            cnpj=fornecedor.cnpj,
            tipo=fornecedor.tipo,
            contato_nome=fornecedor.contato_nome,
            contato_email=fornecedor.contato_email
        )
        db.add(db_fornecedor)
        db.commit()
        db.refresh(db_fornecedor)
        return db_fornecedor

    def delete(self, db: Session, fornecedor_id: int):
        db_obj = self.get_by_id(db, fornecedor_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj