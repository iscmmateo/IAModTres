import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_login_me_refresh():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r1 = await ac.post("/auth/register", json={"email": "user@example.com", "password": "Secret123!"})
        assert r1.status_code == 200
        tokens = r1.json()

        r2 = await ac.post("/auth/login", json={"email": "user@example.com", "password": "Secret123!"})
        assert r2.status_code == 200
        t = r2.json()
        headers = {"Authorization": f"Bearer {t['access_token']}"}

        r3 = await ac.get("/users/me", headers=headers)
        assert r3.status_code == 200
        assert r3.json()["email"] == "user@example.com"

        r4 = await ac.post("/auth/refresh", json={"refresh_token": t["refresh_token"]})
        assert r4.status_code == 200
        assert "access_token" in r4.json()
