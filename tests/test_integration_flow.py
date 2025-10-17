import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_full_auth_flow_and_errors():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/auth/register", json={"email": "flow@example.com", "password": "Secret123!"})
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data and "refresh_token" in data

        r2 = await ac.post("/auth/login", json={"email": "flow@example.com", "password": "Secret123!"})
        assert r2.status_code == 200
        t = r2.json()
        headers = {"Authorization": f"Bearer {t['access_token']}"}

        r3 = await ac.get("/users/me", headers=headers)
        assert r3.status_code == 200
        assert r3.json()["email"] == "flow@example.com"

        r4 = await ac.post("/auth/refresh", json={"refresh_token": t["refresh_token"]})
        assert r4.status_code == 200
        assert "access_token" in r4.json()

        r5 = await ac.post("/auth/login", json={"email": "flow@example.com", "password": "bad"})
        assert r5.status_code == 422 or r5.status_code == 401

        r6 = await ac.get("/users/me", headers={"Authorization": "Bearer invalid"})
        assert r6.status_code in (401, 403)
