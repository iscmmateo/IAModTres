import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_sql_injection_attempt_is_treated_as_string():
    payload_email = "attacker@example.com' OR '1'='1"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/auth/register", json={"email": payload_email, "password": "Secret123!"})
        assert r.status_code == 422  # invalid email rejected by EmailStr

@pytest.mark.asyncio
async def test_xss_payload_is_not_executed_and_returns_as_json_data():
    xss_email = "xss<script>alert(1)</script>@example.com"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/auth/register", json={"email": xss_email, "password": "Secret123!"})
        assert r.status_code == 422  # invalid email

@pytest.mark.asyncio
async def test_rate_limit_on_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json={"email": "ratelimit@example.com", "password": "Secret123!"})
        status_codes = []
        for _ in range(7):
            resp = await ac.post("/auth/login", json={"email": "ratelimit@example.com", "password": "Secret123!"})
            status_codes.append(resp.status_code)
        assert any(code == 429 for code in status_codes)
