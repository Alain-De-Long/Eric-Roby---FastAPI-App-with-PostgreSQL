from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from src.core.config import settings
from src.database.session import get_db
from src.main import app

from tests.helpers.quiz_api import QuizApiClient


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def quiz_api_client(client):
    return QuizApiClient(client, base_url=settings.API_PREFIX)
