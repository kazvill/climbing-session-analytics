import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")
ALGORITHM = "HS256"

# Hash password once at startup
PASSWORD_HASH = pwd_context.hash(APP_PASSWORD)

def create_token():
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

@app.post("/auth/login")
def login(password: str):
    if not pwd_context.verify(password, PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"token": create_token()}

@app.get("/sessions", dependencies=[Depends(verify_token)])
def get_sessions():
    return {
        "sessions": [
            {"date": "2025-01-01", "grade": "V4", "sent": True}
        ]
    }
