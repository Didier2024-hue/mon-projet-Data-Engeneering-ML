# routers/auth.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Literal
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from services.mongo_service import db

router = APIRouter(prefix="/auth", tags=["Auth"])

# === Config via variables d'environnement (chargées dans main.py) ===
JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
AUTH_MODE_DEFAULT = os.getenv("AUTH_MODE", "off").lower()

# === Collection MongoDB ===
users = db["users"]
try:
    users.create_index("username", unique=True)
except Exception:
    pass

# === Modèles Pydantic ===
class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=5, max_length=128)
    role: Literal["admin", "user"] = "user"

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class PublicUser(BaseModel):
    id: str
    username: str
    role: str

# === Hash mot de passe ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(p: str) -> str: return pwd_context.hash(p)
def verify_password(p: str, h: str) -> bool: return pwd_context.verify(p, h)

# === JWT utils ===
def create_access_token(sub: str, role: str, expires_minutes: int = JWT_EXPIRE_MINUTES) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes)
    payload = {"sub": sub, "role": role, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

_bearer_required = HTTPBearer(auto_error=True)   # 401 si pas de header
_bearer_optional = HTTPBearer(auto_error=False)  # n'exige pas de header

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(_bearer_required)) -> PublicUser:
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if not username:
            raise HTTPException(status_code=401, detail="Token invalide (sub manquant)")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    doc = users.find_one({"username": username})
    if not doc:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    return PublicUser(id=str(doc["_id"]), username=doc["username"], role=doc.get("role", "user"))

def current_user_optional(creds: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_optional)) -> Optional[PublicUser]:
    if creds is None:
        return None
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
        doc = users.find_one({"username": username})
        if not doc:
            return None
        return PublicUser(id=str(doc["_id"]), username=doc["username"], role=doc.get("role", "user"))
    except JWTError:
        # ⚠️ important: ne PAS lever 401 ici → on ignore le token invalide
        return None


def guard(level: Literal["sensitive", "full_only"]):
    """
    Sélecteur de dépendance selon AUTH_MODE.
      - off      : rien n'est exigé (optional)
      - partial  : 'sensitive' requis, 'full_only' optionnel
      - full     : tout requis
    """
    mode = os.getenv("AUTH_MODE", AUTH_MODE_DEFAULT).lower()
    if mode == "off":
        return current_user_optional
    if mode == "partial":
        return get_current_user if level == "sensitive" else current_user_optional
    # mode == "full"
    return get_current_user

# === Routes d'auth ===
@router.post("/signup", response_model=PublicUser, status_code=201)
def signup(payload: SignupRequest):
    if users.find_one({"username": payload.username}):
        raise HTTPException(status_code=409, detail="Nom d'utilisateur déjà pris")
    doc = {
        "username": payload.username,
        "password_hash": hash_password(payload.password),
        "role": payload.role,
        "created_at": datetime.utcnow()
    }
    res = users.insert_one(doc)
    return PublicUser(id=str(res.inserted_id), username=payload.username, role=payload.role)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    doc = users.find_one({"username": payload.username})
    if not doc or not verify_password(payload.password, doc.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token(sub=doc["username"], role=doc.get("role", "user"))
    return TokenResponse(access_token=token, expires_in=60 * JWT_EXPIRE_MINUTES)

@router.get("/me", response_model=PublicUser)
def me(user: PublicUser = Depends(get_current_user)):
    return user

