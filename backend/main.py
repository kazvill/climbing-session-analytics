import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://climbing-session-analytics.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Security setup ---
security = HTTPBearer()
ALGORITHM = "HS256"

SECRET_KEY = os.getenv("SECRET_KEY")
PASSWORD_HASH = os.getenv("APP_PASSWORD_HASH")

if not SECRET_KEY or not PASSWORD_HASH:
    raise RuntimeError("Missing environment variables")

def create_token():
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

@app.post("/auth/login")
def login(password: str):
    if not pbkdf2_sha256.verify(password, PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"token": create_token()}

@app.get("/sessions", dependencies=[Depends(verify_token)])
def get_sessions():
    return {
        "sessions": [
            {"date": "2025-01-01", "grade": "V4", "sent": True}
        ]
    }

@app.get("/health")
def health():
    return {"status": "ok"}


