import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def registrar_empresa(client, nome_empresa: str, cnpj: str, email: str) -> dict:
    resposta = client.post(
        "/api/v1/auth/registro",
        json={
            "empresa": {"nome": nome_empresa, "cnpj": cnpj},
            "nome_usuario": "Admin",
            "email": email,
            "senha": "senha-forte-123",
        },
    )
    assert resposta.status_code == 201, resposta.text
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
