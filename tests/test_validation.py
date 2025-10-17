import pytest

@pytest.mark.asyncio
async def test_register_valid_input(client):
    r = await client.post("/auth/register", json={"email": "ok@example.com", "password": "Secret123!"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and "refresh_token" in data

@pytest.mark.asyncio
async def test_register_invalid_email(client):
    r = await client.post("/auth/register", json={"email": "not-an-email", "password": "Secret123!"})
    assert r.status_code == 422  # EmailStr rechaza

@pytest.mark.asyncio
async def test_register_short_password(client):
    r = await client.post("/auth/register", json={"email": "u@example.com", "password": "short"})
    assert r.status_code == 422

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "password": "Secret123!"}
    r1 = await client.post("/auth/register", json=payload)
    assert r1.status_code == 200
    r2 = await client.post("/auth/register", json=payload)
    assert r2.status_code == 400  # “Email already registered”
