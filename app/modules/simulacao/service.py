from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.modules.simulacao.models import SimulacaoModel
from app.modules.simulacao.schemas import CenarioCreate
from app.modules.medicao.models import MedicaoModel
from app.modules.usuario.models import UsuarioModel
from app.core.security import verificar_acesso_unidade


class SimulacaoService:
    def calcular_e_salvar_cenario(self, db: Session, dados: CenarioCreate, usuario: UsuarioModel):
        """
        Executa o cálculo de viabilidade econômica e persiste o cenário
        seguindo os campos definidos no SimulacaoModel do Canvas.
        """
        # 1. Validar se o gestor tem acesso à unidade
        verificar_acesso_unidade(db, dados.unidade_id, usuario)

        # 2. Buscar histórico de consumo real (RF3.5)
        historico = db.query(
            func.extract('month', MedicaoModel.timestamp).label('mes'),
            func.sum(MedicaoModel.consumo_ponta_kwh + MedicaoModel.consumo_fora_ponta_kwh).label('total_kwh')
        ).filter(
            MedicaoModel.unidade_id == dados.unidade_id
        ).group_by('mes').all()

        if not historico:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados de medição insuficientes para realizar a simulação nesta unidade."
            )

        custo_total_anual = 0
        detalhes_mensais = []

        # 3. Motor de Cálculo Financeiro
        for mes_data in historico:
            consumo_mwh = mes_data.total_kwh / 1000

            # Custo do volume contratado no cenário
            custo_contrato = dados.volume_contratado_mwh * dados.preco_contratado_rs

            # Exposição ao PLD (Diferença entre real e contratado)
            diferenca_volume = consumo_mwh - dados.volume_contratado_mwh
            custo_pld = 0

            if diferenca_volume > 0:
                custo_pld = diferenca_volume * dados.pld_medio_estimado_rs
            else:
                # Venda de excedente (simulando 90% do PLD por segurança/spread)
                custo_pld = diferenca_volume * (dados.pld_medio_estimado_rs * 0.9)

            custo_mensal = custo_contrato + custo_pld
            custo_total_anual += custo_mensal

            detalhes_mensais.append({
                "mes": int(mes_data.mes),
                "consumo_mwh": round(consumo_mwh, 2),
                "custo_mensal": round(custo_mensal, 2),
                "balanco_pld_mwh": round(diferenca_volume, 2)
            })

        # 4. Cálculo de Economia (vs. Mercado Cativo hipotético de R$ 650/MWh)
        consumo_total_mwh = sum(d['consumo_mwh'] for d in detalhes_mensais)
        custo_cativo_estimado = consumo_total_mwh * 650.00
        economia = custo_cativo_estimado - custo_total_anual

        # 5. Persistência de acordo com o SimulacaoModel do Canvas
        novo_cenario = SimulacaoModel(
            nome_cenario=dados.nome_cenario,
            unidade_id=dados.unidade_id,
            usuario_id=usuario.id,
            economia_projetada=economia,  # +float economiaProjetada
            custo_total_projetado=custo_total_anual,  # +float custoTotalProjetado
            # Salva os inputs no JSON conforme o diagrama UML (+json parametrosUtilizados)
            parametros_json={
                "volume_mwh": dados.volume_contratado_mwh,
                "preco_base": dados.preco_contratado_rs,
                "pld_estimado": dados.pld_medio_estimado_rs,
                "consumo_total_periodo": consumo_total_mwh
            }
        )

        db.add(novo_cenario)
        db.commit()
        db.refresh(novo_cenario)

        return {
            "id": novo_cenario.id,
            "nome_cenario": novo_cenario.nome_cenario,
            "custo_total_projetado": round(custo_total_anual, 2),
            "economia_projetada": round(economia, 2),
            "custo_medio_mwh": round(custo_total_anual / consumo_total_mwh, 2),
            "detalhes": detalhes_mensais
        }