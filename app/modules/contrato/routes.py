from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import validar_gestor
from app.modules import UsuarioModel
from app.modules.contrato.schemas import ContratoCUSDCreate, ContratoACLCreate, ContratoResponse, ContratoVolumeCreate, \
    ContratoDashboardStats, ContratoListResponse, ContratoDetalheResponse
from app.modules.contrato.repository import ContratoRepository
from app.modules.contrato.service import ContratoService


# Nota: Em um cenário ideal, teríamos um ContratoService aqui também
router = APIRouter(prefix="/contratos", tags=["Contratos (RF1.2)"])
repository = ContratoRepository()
service = ContratoService()


@router.post("/cusd", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato_distribuicao(contrato: ContratoCUSDCreate, db: Session = Depends(get_db)):
    """Novo Contrato de Distribuição (CUSD): Registra o contrato de "Fio" com a Enel. Aqui definimos a Demanda Contratada (Ponta e Fora Ponta), que é o limite de potência que a fábrica pode usar sem pagar multa."""
    return repository.create_cusd(db, contrato)

@router.post("/acl", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato_mercado_livre(contrato: ContratoACLCreate, db: Session = Depends(get_db)):
    """Novo Contrato de Energia (ACL): Registra a compra da energia propriamente dita no Mercado Livre. Definimos preço, volume médio e fonte (ex: Energia Incentivada)."""
    return repository.create_acl(db, contrato)

@router.post("/{contrato_id}/upload", status_code=status.HTTP_201_CREATED)
def upload_contrato_pdf(contrato_id: int, arquivo: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload de PDF do Contrato: Permite anexar o arquivo digital original (PDF) ao cadastro. O sistema salva o arquivo de forma segura no servidor e cria um link de referência no banco de dados."""
    return service.upload_pdf(db, contrato_id, arquivo)

@router.post("/{contrato_id}/volumes", status_code=status.HTTP_201_CREATED)
def adicionar_volumes_mensais(contrato_id: int, volumes: List[ContratoVolumeCreate], db: Session = Depends(get_db)):
    """Sazonalização (Volumes Mensais): Como a indústria não consome igual o ano todo, esta rota permite detalhar o volume contratado mês a mês (Ex: Jan=100, Fev=120), garantindo uma auditoria precisa."""
    return service.adicionar_volumes(db, contrato_id, volumes)

@router.get("/dashboard/stats", response_model=ContratoDashboardStats)
def obter_metricas_contratos(
    db: Session = Depends(get_db),
    gestor_atual: UsuarioModel = Depends(validar_gestor)
):
    """
    Retorna as estatísticas para os cards do Dashboard:
    - Ativos: Contratos em vigor.
    - Vencendo: Contratos que expiram em até 30 dias.
    - Vencidos: Contratos com data fim ultrapassada.
    - Economia Estimada: Soma das projeções de economia das simulações.
    """
    return service.obter_estatisticas_dashboard(db, gestor_atual)

@router.get("/", response_model=List[ContratoListResponse])
def listar_todos_contratos(
    db: Session = Depends(get_db),
    gestor_atual: UsuarioModel = Depends(validar_gestor)
):
    """
    Retorna a lista completa de contratos para a tabela de gestão.
    - Filtra contratos vinculados à empresa do gestor logado.
    - Calcula o status dinâmico (Vigente, Vencendo, Vencido).
    """
    return service.listar_contratos(db, gestor_atual)

@router.get("/{contrato_id}", response_model=ContratoDetalheResponse)
def obter_detalhe_contrato(
    contrato_id: int,
    db: Session = Depends(get_db),
    gestor_atual: UsuarioModel = Depends(validar_gestor)
):
    """
    Retorna as informações detalhadas de um contrato para a vista de 'Detalhes'.
    - Verifica permissão de acesso (ownership).
    - Inclui alertas de vigência e lista de documentos.
    """
    return service.obter_detalhe_por_id(db, contrato_id, gestor_atual)