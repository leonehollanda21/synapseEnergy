from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CenarioCreate(BaseModel):
    nome_cenario: str
    unidade_id: int
    volume_contratado_mwh: float
    preco_contratado_rs: float
    pld_medio_estimado_rs: float

class DetalheMensalSimulacao(BaseModel):
    mes: int
    consumo_mwh: float
    custo_mensal: float
    balanco_pld_mwh: float

class SimulacaoResponse(BaseModel):
    id: Optional[int] = None
    nome_cenario: str
    custo_total_projetado: float  # Sincronizado com o Service/Model
    economia_projetada: float      # Sincronizado com o Service/Model
    custo_medio_mwh: float
    detalhes: List[DetalheMensalSimulacao] # Sincronizado com o campo 'detalhes' do Service

    class Config:
        from_attributes = True