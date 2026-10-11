import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import Base, engine
import asyncio

@pytest.fixture(scope="session", autouse=True)
def reset_db():
    async def _reset():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(_reset())

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_payload():
    return  {
        "username": "testuser",
        "email": "tima@test.com",
        "password": "Super-key123",
    }


@pytest.fixture
def registered_user(client, user_payload):
    client.post('/auth/register', json=user_payload)
    return user_payload

@pytest.fixture
def auth_headers(client, user_payload):
    response = client.post('/auth/token', data={
        "username": user_payload["username"],
        "password": user_payload["password"],
    })

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
