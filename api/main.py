from dotenv import load_dotenv
load_dotenv("/home/datascientest/cde/api/.env.api")

from fastapi import FastAPI
from datetime import datetime
from routers import default, societes, commentaires, predict
from routers import auth

app = FastAPI()

# ============================================
# AJOUT MINIMAL POUR GRAFANA
# ============================================
@app.get("/health")
async def health_check():
    """Endpoint de santé minimal pour Grafana"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# ============================================
# ROUTERS EXISTANTS (NE PAS TOUCHER)
# ============================================
app.include_router(default.router)
app.include_router(societes.router)
app.include_router(commentaires.router)
# app.include_router(export.router) # supprimé à la demande tuteur
app.include_router(predict.router)
app.include_router(auth.router)