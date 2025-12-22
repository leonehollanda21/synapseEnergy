from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.medicao.schemas import MedicaoCreate, DashboardStats, GraficoPontoResponse
from app.modules.medicao.service import MedicaoService

router = APIRouter(prefix="/medicao", tags=["Monitoramento e Consumo (RF2.2 - RF2.6)"])
service = MedicaoService()

@router.post("/manual", status_code=status.HTTP_201_CREATED)
def inserir_medicao_manual(medicao: MedicaoCreate, db: Session = Depends(get_db)):
    """Insere um registro de medição manual (RF2.2 via API)."""
    service.registrar_medicao(db, medicao)
    return {"message": "Medição registrada com sucesso"}

@router.get("/dashboard/{unidade_id}", response_model=DashboardStats)
def obter_dashboard(unidade_id: int, db: Session = Depends(get_db)):
    """
    Dashboard de Decisão (KPIs): É a tela principal do gestor. O sistema cruza o Total Consumido (do CSV) contra o Total Contratado (do Módulo 1) e calcula automaticamente o Balanço Energético e a Exposição Financeira (R$), alertando sobre riscos de prejuízo.
    """
    return service.calcular_dashboard(db, unidade_id)

@router.get("/historico/{unidade_id}", response_model=List[GraficoPontoResponse])
def obter_historico_grafico(unidade_id: int, db: Session = Depends(get_db)):
    """
    Série Histórica (Gráfico): Fornece os dados estruturados (Dia x Consumo) para renderizar o gráfico de linha, permitindo ao analista visualizar a curva de consumo da fábrica ao longo do tempo.
    """
    return service.obter_historico_grafico(db, unidade_id)