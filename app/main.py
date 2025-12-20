from fastapi import FastAPI
from app.core.database import engine, Base

# --- PONTO CRUCIAL ---
# Importando os modelos AQUI, o Python executa o arquivo app/modules.py
# e registra as classes (EmpresaModel, etc) dentro da Base.
import app.modules

# Agora que a Base conhece os modelos, o create_all vai funcionar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Synapse Energia API")

@app.get("/")
def read_root():
    return {"message": "Tabelas criadas com sucesso e API Synapse rodando! 🚀"}