from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date


# Para receber dados via API (simulando upload)
class MedicaoCreate(BaseModel):
    timestamp: datetime
    consumo_ponta_kwh: float
    consumo_fora_ponta_kwh: float
    demanda_medida_kw: float
    unidade_id: int

# Para o Dashboard (RF2.3 e RF2.4)
class DashboardStats(BaseModel):
    total_consumido_mwh: float
    total_contratado_mwh: float
    balanco_energetico_mwh: float # Sobra ou Déficit
    status: str # "DÉFICIT", "SOBRA", "EQUILIBRADO"
    exposicao_financeira_estimada: float # Custo do PLD

class GraficoPontoResponse(BaseModel):
    data: date
    consumo_total_mwh: float

    class Config:
        from_attributes = True