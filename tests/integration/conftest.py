import pytest
from fastapi.testclient import TestClient
from src.core.config import settings
from src.database.session import SessionLocal, create_all_tables, engine, get_db
from src.main import app

from tests.helpers.quiz_api import QuizApiClient


@pytest.fixture(scope="session", autouse=True)
def setup_integration_database():
    create_all_tables()

    yield


@pytest.fixture(scope="function")
def integration_db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def integration_client(integration_db_session):
    def _override_get_db():
        yield integration_db_session

    app.dependency_overrides[get_db] = _override_get_db

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def integration_quiz_api(integration_client):
    base_url = f"{settings.ENDPOINT}{settings.API_PREFIX}"
    return QuizApiClient(client=integration_client, base_url=base_url)
