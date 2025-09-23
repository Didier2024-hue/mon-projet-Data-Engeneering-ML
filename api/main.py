from fastapi import FastAPI
from routers import default, societes, commentaires, export, predict

app = FastAPI()

# Importation des routeurs
app.include_router(default.router)
app.include_router(societes.router)
app.include_router(commentaires.router)
app.include_router(export.router)
app.include_router(predict.router)
