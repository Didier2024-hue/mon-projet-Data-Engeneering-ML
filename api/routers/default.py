from fastapi import APIRouter

router = APIRouter(tags=["Default"])

@router.get("/", summary="Root endpoint")
def root():
    return {"message": "Bienvenue sur l'API Trustpilot"}

@router.get("/health", summary="Healthcheck endpoint")
def health():
    return {"status": "ok"}
