import jwt
import pytest
from datetime import datetime, timedelta, timezone
from app.security import create_access_token, create_refresh_token, decode_jwt
from app.config import settings

def test_access_jwt_contains_expected_claims():
    token = create_access_token(42, "user@example.com")
    payload = decode_jwt(token)
    assert payload is not None
    assert payload["type"] == "access"
    assert payload["sub"] == "42"
    assert payload["email"] == "user@example.com"
    assert "exp" in payload

def test_refresh_jwt_type_is_refresh():
    token = create_refresh_token(7, "r@example.com")
    p = decode_jwt(token)
    assert p is not None and p["type"] == "refresh"

def test_jwt_invalid_signature():
    token = create_access_token(1, "a@b.com")
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "WRONG_SECRET", algorithms=[settings.JWT_ALG])

def test_jwt_expired_returns_none():
    exp = datetime.now(timezone.utc) - timedelta(seconds=2)
    payload = {"sub": "1", "email": "x@y.com", "type": "access", "exp": exp}
    bad = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    assert decode_jwt(bad) is None

@pytest.mark.asyncio
async def test_refresh_endpoint_requires_refresh_type(client):
    await client.post("/auth/register", json={"email": "t@example.com", "password": "Secret123!"})
    login = await client.post("/auth/login", json={"email": "t@example.com", "password": "Secret123!"})
    access = login.json()["access_token"]  # usar access en refresh a propósito
    r = await client.post("/auth/refresh", json={"refresh_token": access})
    assert r.status_code == 401
