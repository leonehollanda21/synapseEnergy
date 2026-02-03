from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date

from app.modules import UsuarioModel
from app.modules.medicao.models import MedicaoModel
from app.modules.medicao.schemas import DashboardStats, MedicaoCreate
from app.core.security import verificar_acesso_unidade


class MedicaoService:
    def registrar_medicao(self, db: Session, dados: MedicaoCreate
                          #, usuario_logado: UsuarioModel
                          ):
        #verificar_acesso_unidade(db, dados.unidade_id, usuario_logado)

        nova_medicao = MedicaoModel(**dados.dict())
        db.add(nova_medicao)
        db.commit()
        db.refresh(nova_medicao)
        return nova_medicao

    def calcular_dashboard(self, db: Session, unidade_id: int) -> DashboardStats:
        total_consumo = db.query(
            func.sum(MedicaoModel.consumo_ponta_kwh + MedicaoModel.consumo_fora_ponta_kwh)
        ).filter(MedicaoModel.unidade_id == unidade_id).scalar() or 0.0

        total_consumo_mwh = total_consumo / 1000.0

        total_contratado_mwh = 500.0

        balanco = total_contratado_mwh - total_consumo_mwh

        pld_atual = 250.00  # R$/MWh (Preço de mercado simulado)

        if balanco < 0:
            status = "DÉFICIT (RISCO)"
            exposicao = abs(balanco) * pld_atual
        else:
            status = "SOBRA"
            exposicao = balanco * pld_atual

        return DashboardStats(
            total_consumido_mwh=round(total_consumo_mwh, 2),
            total_contratado_mwh=round(total_contratado_mwh, 2),
            balanco_energetico_mwh=round(balanco, 2),
            status=status,
            exposicao_financeira_estimada=round(exposicao, 2)
        )

    def obter_historico_grafico(self, db: Session, unidade_id: int):
        dados = db.query(
            cast(MedicaoModel.timestamp, Date).label('data'),
            func.sum(MedicaoModel.consumo_ponta_kwh + MedicaoModel.consumo_fora_ponta_kwh).label('total_kwh')
        ).filter(
            MedicaoModel.unidade_id == unidade_id
        ).group_by(
            cast(MedicaoModel.timestamp, Date)
        ).order_by(
            cast(MedicaoModel.timestamp, Date)
        ).all()

        resultado = []
        for linha in dados:
            resultado.append({
                "data": linha.data,
                "consumo_total_mwh": (linha.total_kwh or 0) / 1000.0  # Convertendo kWh para MWh
            })
        return resultado