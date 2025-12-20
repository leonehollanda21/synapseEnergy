from app.modules.empresa.models import EmpresaModel
from app.modules.usuario.models import UsuarioModel
from app.modules.fornecedor.models import FornecedorModel
from app.modules.unidadeConsumidora.models import UnidadeConsumidoraModel # ou unidadeConsumidoraModel

# --- CONTRATOS ---
from app.modules.contrato.models import ContratoModel
# Usando o nome da pasta que apareceu na sua imagem 'contradorCUSD'
from app.modules.contradorCUSD.models import ContratoCUSDModel
from app.modules.contratoACL.models import ContratoACLModel
from app.modules.documento.models import DocumentoModel
from app.modules.alerta.models import AlertaModel

# --- MONITORAMENTO ---
from app.modules.medicao.models import MedicaoModel

# --- INTELIGÊNCIA ---
from app.modules.pedidoCotacao.models import PedidoCotacaoModel # ou rfqModel
from app.modules.proposta.models import PropostaModel
from app.modules.simulacao.models import SimulacaoModel