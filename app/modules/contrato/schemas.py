from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.modules.contrato.enums import StatusContratoEnum


# Schema Base para Contratos
class ContratoBase(BaseModel):
    data_inicio: date
    data_fim: date
    data_assinatura: Optional[date] = None
    status: StatusContratoEnum = StatusContratoEnum.RASCUNHO

    # IDs de relacionamento
    unidade_id: int
    fornecedor_id: int


# Schema específico para criar Contrato CUSD (Distribuidora)
class ContratoCUSDCreate(ContratoBase):
    tipo_contrato: str = "cusd"  # Discriminador fixo
    demanda_ponta_kw: float
    demanda_fora_ponta_kw: float
    subgrupo_tarifario: str


# Schema específico para criar Contrato ACL (Mercado Livre)
class ContratoACLCreate(ContratoBase):
    tipo_contrato: str = "acl"  # Discriminador fixo
    volume_mensal_mwh: float
    preco_mwh: float
    flexibilidade_min: Optional[float] = None
    flexibilidade_max: Optional[float] = None
    fonte_energia: str


# Schema de Resposta (simplificado para visualização geral)
class ContratoResponse(ContratoBase):
    id: int
    tipo_contrato: str

    class Config:
        from_attributes = True


# --- SCHEMA PARA SAZONALIZAÇÃO (RF1.3) ---
# Este schema define o formato de UM mês de volume.
# Ele NÃO é uma tabela, é apenas a validação de dados.
class ContratoVolumeCreate(BaseModel):
    ano: int
    mes: int
    volume_mwh: float
    preco_mwh: float