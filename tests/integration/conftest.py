import pytest
from fastapi.testclient import TestClient
from src.core.config import settings
from src.database.session import create_all_tables
from src.main import app

from tests.helpers.quiz_api import QuizApiClient


@pytest.fixture(scope="session", autouse=True)
def setup_integration_database():
    create_all_tables()

    yield


@pytest.fixture(scope="session")
def integration_client():
    yield TestClient(app)


@pytest.fixture(scope="session")
def integration_quiz_api(integration_client):
    base_url = f"{settings.ENDPOINT}{settings.API_PREFIX}"
    return QuizApiClient(client=integration_client, base_url=base_url)
