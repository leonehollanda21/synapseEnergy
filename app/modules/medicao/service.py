from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from app.modules.medicao.models import MedicaoModel
from app.modules.medicao.schemas import DashboardStats, MedicaoCreate


class MedicaoService:
    def registrar_medicao(self, db: Session, dados: MedicaoCreate):
        nova_medicao = MedicaoModel(**dados.dict())
        db.add(nova_medicao)
        db.commit()
        return nova_medicao

    def calcular_dashboard(self, db: Session, unidade_id: int) -> DashboardStats:
        # 1. Busca total consumido no banco (Soma de ponta + fora ponta)
        # Nota: Convertendo kWh para MWh (dividindo por 1000)
        total_consumo = db.query(
            func.sum(MedicaoModel.consumo_ponta_kwh + MedicaoModel.consumo_fora_ponta_kwh)
        ).filter(MedicaoModel.unidade_id == unidade_id).scalar() or 0.0

        total_consumo_mwh = total_consumo / 1000.0

        # 2. Busca total contratado (Simulado/Mockado por enquanto, pois precisaria cruzar com Módulo Contrato)
        # Futuramente: Buscaria no ContratoACLModel vigente para esta unidade
        total_contratado_mwh = 500.0  # Exemplo: Empresa contratou 500 MWh

        # 3. Calcula Balanço
        balanco = total_contratado_mwh - total_consumo_mwh

        # 4. Define Status e Calcula Exposição (RF2.4)
        pld_atual = 250.00  # R$/MWh (Preço de mercado simulado)

        if balanco < 0:
            status = "DÉFICIT (RISCO)"
            # Se consumiu mais que contratou, paga PLD sobre a diferença
            exposicao = abs(balanco) * pld_atual
        else:
            status = "SOBRA"
            # Se sobrou, pode vender ao PLD (receita potencial)
            exposicao = balanco * pld_atual  # Positivo seria receita

        return DashboardStats(
            total_consumido_mwh=round(total_consumo_mwh, 2),
            total_contratado_mwh=round(total_contratado_mwh, 2),
            balanco_energetico_mwh=round(balanco, 2),
            status=status,
            exposicao_financeira_estimada=round(exposicao, 2)
        )

    def obter_historico_grafico(self, db: Session, unidade_id: int):
        """
        Agrupa o consumo por dia para alimentar o gráfico de linha.
        Retorna: Lista de {data, consumo_total_mwh}
        """
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

        # Formata o retorno
        resultado = []
        for linha in dados:
            resultado.append({
                "data": linha.data,
                "consumo_total_mwh": (linha.total_kwh or 0) / 1000.0  # Convertendo kWh para MWh
            })
        return resultado