from pydantic import BaseModel, EmailStr
from typing import Optional

class EmpresaBase(BaseModel):
    razao_social: str
    cnpj: str
    setor_atuacao: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int

    class Config:
        from_attributes = True

class GestorCreate(BaseModel):
    nome: str
    email: str
    senha: str

class CadastroEmpresaConsumidoraRequest(BaseModel):
    empresa: EmpresaCreate
    gestor: GestorCreate