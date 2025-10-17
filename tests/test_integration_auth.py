import pytest

@pytest.mark.asyncio
async def test_full_auth_flow(client):
    r1 = await client.post("/auth/register", json={"email": "flow@example.com", "password": "Secret123!"})
    assert r1.status_code == 200
    t1 = r1.json()

    r2 = await client.post("/auth/login", json={"email": "flow@example.com", "password": "Secret123!"})
    assert r2.status_code == 200
    t2 = r2.json()

    headers = {"Authorization": f"Bearer {t2['access_token']}"}
    r3 = await client.get("/users/me", headers=headers)
    assert r3.status_code == 200
    assert r3.json()["email"] == "flow@example.com"

    r4 = await client.post("/auth/refresh", json={"refresh_token": t2["refresh_token"]})
    assert r4.status_code == 200
    assert "access_token" in r4.json()

@pytest.mark.asyncio
async def test_invalid_credentials_and_invalid_bearer(client):
    await client.post("/auth/register", json={"email": "nogood@example.com", "password": "Secret123!"})

    bad = await client.post("/auth/login", json={"email": "nogood@example.com", "password": "Wrong!"})
    assert bad.status_code in (401, 422)

    r = await client.get("/users/me", headers={"Authorization": "Bearer garbage"})
    assert r.status_code in (401, 403)
