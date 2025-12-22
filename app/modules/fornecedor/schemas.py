from pydantic import BaseModel, EmailStr
from typing import Optional
from app.modules.fornecedor.enums import TipoFornecedorEnum

class FornecedorBase(BaseModel):
    razao_social: str
    cnpj: str
    tipo: TipoFornecedorEnum
    contato_nome: Optional[str] = None
    contato_email: Optional[EmailStr] = None

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(BaseModel):
    razao_social: Optional[str] = None
    tipo: Optional[TipoFornecedorEnum] = None
    contato_nome: Optional[str] = None
    contato_email: Optional[EmailStr] = None

class FornecedorResponse(FornecedorBase):
    id: int

    class Config:
        from_attributes = True