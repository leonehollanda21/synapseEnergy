from sqlalchemy.orm import Session
from typing import List

from app.modules import ContratoModel, ContratoCUSDModel, DocumentoModel, ContratoACLModel
from app.modules.contrato.schemas import ContratoCUSDCreate, ContratoACLCreate, ContratoVolumeCreate
from app.modules.contratoVolume.models import ContratoVolumeModel


class ContratoRepository:

    def get_by_id(self, db: Session, contrato_id: int):
        return db.query(ContratoModel).filter(ContratoModel.id == contrato_id).first()

    def create_cusd(self, db: Session, contrato: ContratoCUSDCreate):
        db_contrato = ContratoCUSDModel(
            data_inicio=contrato.data_inicio,
            data_fim=contrato.data_fim,
            data_assinatura=contrato.data_assinatura,
            status=contrato.status,
            unidade_id=contrato.unidade_id,
            fornecedor_id=contrato.fornecedor_id,
            demanda_ponta_kw=contrato.demanda_ponta_kw,
            demanda_fora_ponta_kw=contrato.demanda_fora_ponta_kw,
            subgrupo_tarifario=contrato.subgrupo_tarifario
        )
        db.add(db_contrato)
        db.commit()
        db.refresh(db_contrato)
        return db_contrato

    def create_acl(self, db: Session, contrato: ContratoACLCreate):
        db_contrato = ContratoACLModel(
            data_inicio=contrato.data_inicio,
            data_fim=contrato.data_fim,
            data_assinatura=contrato.data_assinatura,
            status=contrato.status,
            unidade_id=contrato.unidade_id,
            fornecedor_id=contrato.fornecedor_id,
            volume_mensal_mwh=contrato.volume_mensal_mwh,
            preco_mwh=contrato.preco_mwh,
            flexibilidade_min=contrato.flexibilidade_min,
            flexibilidade_max=contrato.flexibilidade_max,
            fonte_energia=contrato.fonte_energia
        )
        db.add(db_contrato)
        db.commit()
        db.refresh(db_contrato)
        return db_contrato

    def create_documento(self, db: Session, nome_arquivo: str, caminho: str, data_upload, contrato_id: int):
        novo_doc = DocumentoModel(
            nome_arquivo=nome_arquivo,
            caminho_url=caminho,  # Usando o nome da sua coluna
            data_upload=data_upload,
            contrato_id=contrato_id
        )
        db.add(novo_doc)
        db.commit()
        db.refresh(novo_doc)
        return novo_doc

    def create_volumes_mensais(self, db: Session, contrato_id: int, volumes: List[ContratoVolumeCreate]):
        objetos_db = []
        for vol in volumes:
            novo_vol = ContratoVolumeModel(
                contrato_id=contrato_id,
                ano=vol.ano,
                mes=vol.mes,
                volume_mwh=vol.volume_mwh,
                preco_mwh=vol.preco_mwh
            )
            objetos_db.append(novo_vol)

        db.add_all(objetos_db)
        db.commit()
        return len(objetos_db)