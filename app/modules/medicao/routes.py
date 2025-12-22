from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.medicao.schemas import MedicaoCreate, DashboardStats
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
    Retorna os dados consolidados para o painel principal (RF2.3 e RF2.4).
    Calcula balanço energético e exposição financeira.
    """
    return service.calcular_dashboard(db, unidade_id)