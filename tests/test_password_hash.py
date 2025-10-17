from app.security import hash_password, verify_password

def test_password_hash_and_verify_success():
    plain = "Secret123!"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True

def test_password_hash_and_verify_fail():
    hashed = hash_password("Secret123!")
    assert verify_password("WrongPass!", hashed) is False
