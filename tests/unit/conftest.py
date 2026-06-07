import pytest
from src.core.config import settings

from tests.helpers.quiz_api import QuizApiClient


@pytest.fixture
def quiz_api_client(client):
    return QuizApiClient(client, base_url=settings.API_PREFIX)
