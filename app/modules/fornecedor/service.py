from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.fornecedor.repository import FornecedorRepository
from app.modules.fornecedor.schemas import FornecedorCreate

class FornecedorService:
    def __init__(self):
        self.repository = FornecedorRepository()

    def criar_fornecedor(self, db: Session, fornecedor: FornecedorCreate):
        # Regra de Negócio: Não permitir CNPJ duplicado
        existe = self.repository.get_by_cnpj(db, fornecedor.cnpj)
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fornecedor com este CNPJ já cadastrado."
            )
        return self.repository.create(db, fornecedor)

    def listar_fornecedores(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.get_all(db, skip, limit)