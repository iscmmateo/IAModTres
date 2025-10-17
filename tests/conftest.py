import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import SessionLocal
from app.models import User

@pytest.fixture(autouse=True)
def _cleanup_db():
    """Limpia la tabla de usuarios antes de cada test (estado determinista)."""
    db: Session = SessionLocal()
    try:
        db.query(User).delete()
        db.commit()
        yield
    finally:
        db.close()

@pytest.fixture
async def client():
    """Cliente HTTP asíncrono para llamar a la API."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
