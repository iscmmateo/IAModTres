from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import RegisterIn, LoginIn, TokenOut
from ..security import hash_password, verify_password, create_access_token, create_refresh_token
from ..rate_limit import limiter
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

# Registro
@router.post("/register", response_model=TokenOut)
@limiter.limit(settings.RATE_LIMIT_LOGIN)  # usa el valor del .env
def register(request: Request, payload: RegisterIn, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    u = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return TokenOut(
        access_token=create_access_token(u.id, u.email),
        refresh_token=create_refresh_token(u.id, u.email),
    )

# Inicio de sesión
@router.post("/login", response_model=TokenOut)
@limiter.limit(settings.RATE_LIMIT_LOGIN)
def login(request: Request, payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return TokenOut(
        access_token=create_access_token(user.id, user.email),
        refresh_token=create_refresh_token(user.id, user.email),
    )

# Refrescar token
@router.post("/refresh", response_model=dict)
def refresh(payload: dict):
    from ..security import decode_jwt, create_access_token
    token = payload.get("refresh_token")
    data = decode_jwt(token)
    if not data or data.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    new_access = create_access_token(int(data["sub"]), data["email"])
    return {"access_token": new_access, "token_type": "bearer"}
