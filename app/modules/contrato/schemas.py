from pydantic import BaseModel
from typing import Optional, List
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


class ContratoVolumeCreate(BaseModel):
    ano: int
    mes: int
    volume_mwh: float
    preco_mwh: float


class ContratoDashboardStats(BaseModel):
    ativos: int
    vencendo: int
    vencidos: int
    economia_estimada: float

class ContratoListResponse(BaseModel):
    id: int
    tipo: str
    fornecedor: str
    vigencia: str
    data_inicio: date
    data_fim: date
    status: str
    valor_total: Optional[float] = 0.0 #
    unidade_nome: str

    class Config:
        from_attributes = True


class DocumentoAnexoResponse(BaseModel):
    id: int
    nome_arquivo: str
    url: Optional[str] = None

    class Config:
        from_attributes = True

class ContratoDetalheResponse(BaseModel):
    id: int
    tipo_contrato: str # Alterado de 'tipo' para 'tipo_contrato'
    fornecedor_nome: str
    data_inicio: date
    data_fim: date
    status: str
    unidade_nome: str
    alerta_vigencia: str
    documentos: List[DocumentoAnexoResponse] = []

    class Config:
        from_attributes = True