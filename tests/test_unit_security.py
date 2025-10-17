import pytest
from app.security import hash_password, verify_password, create_access_token, decode_jwt
from datetime import timedelta, datetime, timezone
import jwt

def test_password_hash_and_verify():
    plain = "Secret123!"
    h = hash_password(plain)
    assert h != plain
    assert verify_password(plain, h) is True
    assert verify_password("WrongPass!", h) is False

def test_jwt_create_and_decode():
    token = create_access_token(1, "user@example.com")
    payload = decode_jwt(token)
    assert payload is not None
    assert payload.get("type") == "access"
    assert payload.get("email") == "user@example.com"

def test_jwt_invalid_signature(monkeypatch):
    token = create_access_token(1, "user@example.com")
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "wrong-secret", algorithms=["HS256"])

def test_jwt_expired():
    exp = datetime.now(timezone.utc) - timedelta(seconds=1)
    payload = {"sub": "1", "email": "user@example.com", "type": "access", "exp": exp}
    bad = jwt.encode(payload, "change-me", algorithm="HS256")
    assert decode_jwt(bad) is None
