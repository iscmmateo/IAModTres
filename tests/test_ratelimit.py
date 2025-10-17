import pytest

@pytest.mark.asyncio
async def test_rate_limit_login(client):
    await client.post("/auth/register", json={"email": "rl@example.com", "password": "Secret123!"})
    codes = []
    for _ in range(8):
        res = await client.post("/auth/login", json={"email": "rl@example.com", "password": "Secret123!"})
        codes.append(res.status_code)
    assert any(c == 429 for c in codes)

@pytest.mark.asyncio
async def test_rate_limit_register(client):
    codes = []
    for i in range(8):
        res = await client.post("/auth/register", json={"email": f"rlr{i}@example.com", "password": "Secret123!"})
        codes.append(res.status_code)
    assert any(c == 429 for c in codes)
