from dotenv import load_dotenv
load_dotenv("/home/datascientest/cde/api/.env.api")

from fastapi import FastAPI
from routers import default, societes, commentaires, export, predict
from routers import auth

app = FastAPI()

# Importation des routeurs
app.include_router(default.router)
app.include_router(societes.router)
app.include_router(commentaires.router)
app.include_router(export.router)
app.include_router(predict.router)
app.include_router(auth.router)

