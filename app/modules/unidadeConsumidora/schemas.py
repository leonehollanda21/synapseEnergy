from pydantic import BaseModel
from typing import Optional

class UnidadeBase(BaseModel):
    nome: str
    codigo_ccee: str
    endereco: Optional[str] = None
    tensao_fornecimento: float

class UnidadeCreate(UnidadeBase):
    pass

class UnidadeResponse(UnidadeBase):
    id: int

    class Config:
        from_attributes = True