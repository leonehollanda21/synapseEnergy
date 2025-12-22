from fastapi import FastAPI
from app.core.database import engine, Base

# --- PONTO CRUCIAL ---
# Importando os modelos AQUI, o Python executa o arquivo app/modules.py
# e registra as classes (EmpresaModel, etc) dentro da Base.
import app.modules


from app.modules.fornecedor.routes import router as fornecedor_router
from app.modules.contrato.routes import router as contrato_router
from app.modules.unidadeConsumidora.routes import router as unidade_router
from app.modules.medicao.routes import router as medicao_router

# Agora que a Base conhece os modelos, o create_all vai funcionar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Synapse Energia API",
    description="Sistema de Gestão para Consumidores do Grupo A no Mercado Livre",
    version="1.0.0"
)

# --- 5. REGISTRO DAS ROTAS ---
app.include_router(fornecedor_router)
app.include_router(contrato_router)
app.include_router(unidade_router)
app.include_router(medicao_router)
@app.get("/")
def read_root():
    return {"message": "Tabelas criadas com sucesso e API Synapse rodando! 🚀"}