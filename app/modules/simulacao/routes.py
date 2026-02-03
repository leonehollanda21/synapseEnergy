from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.simulacao.schemas import CenarioCreate, SimulacaoResponse
from app.modules.simulacao.service import SimulacaoService
from app.modules.usuario.models import UsuarioModel
from app.core.security import validar_gestor

router = APIRouter(prefix="/simulador", tags=["Inteligência e Simulação (RF3.4)"])
service = SimulacaoService()


@router.post("/gerar-cenario", response_model=SimulacaoResponse)
def criar_simulacao_estrategica(
        dados: CenarioCreate,
        db: Session = Depends(get_db),
        gestor: UsuarioModel = Depends(validar_gestor)
):
    """
    RF3.4 & RF3.5: Gera uma simulação de custos baseada em premissas de mercado
    e no histórico real de consumo da unidade.

    Retorna o JSON completo com os valores salvos e os cálculos detalhados.
    """
    # A chamada do service deve retornar o dicionário com:
    # id, nome_cenario, custo_total_projetado, economia_projetada, custo_medio_mwh e detalhes
    return service.calcular_e_salvar_cenario(db, dados, gestor)