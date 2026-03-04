from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
import shutil
import os
from datetime import date, timedelta
from typing import List

from app.modules import ContratoModel, UsuarioModel, SimulacaoModel, UnidadeConsumidoraModel
from app.modules.contrato.repository import ContratoRepository
from app.modules.contrato.schemas import ContratoVolumeCreate

UPLOAD_DIR = "uploads/contratos"


class ContratoService:
    def __init__(self):
        self.repository = ContratoRepository()
        # Garante que a pasta existe ao iniciar o serviço
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def upload_pdf(self, db: Session, contrato_id: int, arquivo: UploadFile):
        # 1. Validação: Contrato existe?
        contrato = self.repository.get_by_id(db, contrato_id)
        if not contrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato não encontrado"
            )

        # 2. Define caminho físico
        caminho_arquivo = f"{UPLOAD_DIR}/{contrato_id}_{arquivo.filename}"

        # 3. Lógica de Arquivo (IO)
        try:
            with open(caminho_arquivo, "wb") as buffer:
                shutil.copyfileobj(arquivo.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar arquivo: {str(e)}"
            )

        # 4. Chama repositório para salvar metadados
        return self.repository.create_documento(
            db=db,
            nome_arquivo=arquivo.filename,
            caminho=caminho_arquivo,
            data_upload=date.today(),
            contrato_id=contrato_id
        )

    def adicionar_volumes(self, db: Session, contrato_id: int, volumes: List[ContratoVolumeCreate]):
        # 1. Validação
        contrato = self.repository.get_by_id(db, contrato_id)
        if not contrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato não encontrado"
            )

        # 2. Chama repositório
        qtd_adicionada = self.repository.create_volumes_mensais(db, contrato_id, volumes)
        return {"message": f"{qtd_adicionada} registros de volume adicionados."}

    def obter_estatisticas_dashboard(self, db: Session, usuario: UsuarioModel):
        """
        Calcula os indicadores para o dashboard baseados na data atual.
        Filtra apenas contratos da empresa do usuário logado.
        """
        hoje = date.today()
        proximos_30_dias = hoje + timedelta(days=30)

        query_base = db.query(ContratoModel).join(UnidadeConsumidoraModel).filter(
            UnidadeConsumidoraModel.empresa_id == usuario.empresa_id
        )

        ativos = query_base.filter(
            ContratoModel.data_inicio <= hoje,
            ContratoModel.data_fim >= hoje
        ).count()

        vencendo = query_base.filter(
            ContratoModel.data_fim >= hoje,
            ContratoModel.data_fim <= proximos_30_dias
        ).count()

        vencidos = query_base.filter(
            ContratoModel.data_fim < hoje
        ).count()

        economia_total = db.query(func.sum(SimulacaoModel.economia_projetada)).filter(
            SimulacaoModel.usuario_id == usuario.id
        ).scalar() or 0.0

        return {
            "ativos": ativos,
            "vencendo": vencendo,
            "vencidos": vencidos,
            "economia_estimada": round(float(economia_total), 2)
        }

    def listar_contratos(self, db: Session, usuario: UsuarioModel):
        """
        Retorna a lista completa de contratos para a tabela de gestão.
        Calcula o status dinâmico para cada contrato com base na data atual.
        """
        hoje = date.today()
        proximos_30_dias = hoje + timedelta(days=30)

        # Busca todos os contratos vinculados às unidades da empresa do utilizador
        contratos = db.query(ContratoModel).join(UnidadeConsumidoraModel).filter(
            UnidadeConsumidoraModel.empresa_id == usuario.empresa_id
        ).all()

        resultado = []
        for c in contratos:
            # Lógica para determinar o status conforme o ecrã de Contratos de Energia
            if c.data_fim < hoje:
                status_label = "Vencido"
            elif hoje <= c.data_fim <= proximos_30_dias:
                status_label = "Vencendo"
            else:
                status_label = "Vigente"

            resultado.append({
                "id": c.id,
                "tipo": getattr(c, 'tipo', 'N/A'),  # ACL ou CUSD
                "fornecedor": c.fornecedor.razao_social if c.fornecedor else "Não informado",
                "vigencia": f"{c.data_inicio.strftime('%Y-%m-%d')} → {c.data_fim.strftime('%Y-%m-%d')}",
                "data_inicio": c.data_inicio,
                "data_fim": c.data_fim,
                "status": status_label,
                #"valor_total": c.valor_total,
                "unidade_nome": c.unidade.nome if c.unidade else "N/A"
            })

        return resultado

    def obter_detalhe_por_id(self, db: Session, contrato_id: int, usuario: UsuarioModel):
        """
        RF1.2: Obtém os detalhes completos de um contrato específico.
        Valida se a unidade do contrato pertence à empresa do gestor.
        """
        hoje = date.today()
        proximos_30_dias = hoje + timedelta(days=30)

        # Busca o contrato com os relacionamentos necessários
        contrato = db.query(ContratoModel).join(UnidadeConsumidoraModel).filter(
            ContratoModel.id == contrato_id,
            UnidadeConsumidoraModel.empresa_id == usuario.empresa_id
        ).first()

        if not contrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato não encontrado ou sem permissão de acesso."
            )

        # Lógica de Status (Mesma da lista e dashboard)
        if contrato.data_fim < hoje:
            status_label = "Vencido"
            alerta = "Este contrato está vencido."
        elif hoje <= contrato.data_fim <= proximos_30_dias:
            status_label = "Vencendo"
            alerta = "Este contrato expira em breve."
        else:
            status_label = "Vigente"
            alerta = "Contrato dentro do prazo de vigência."

        return {
            "id": contrato.id,
            "tipo_contrato": contrato.tipo_contrato,  # CORRIGIDO AQUI
            "fornecedor_nome": contrato.fornecedor.razao_social if contrato.fornecedor else "Não informado",
            "data_inicio": contrato.data_inicio,
            "data_fim": contrato.data_fim,
            "status": status_label,
            "unidade_nome": contrato.unidade.nome if contrato.unidade else "N/A",
            "alerta_vigencia": alerta,
            "documentos": [
                {"id": doc.id, "nome_arquivo": doc.nome_arquivo}
                for doc in contrato.documentos
            ] if contrato.documentos else []
        }