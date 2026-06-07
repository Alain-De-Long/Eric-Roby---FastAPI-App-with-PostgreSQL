from unittest.mock import MagicMock

import pytest
from src.core.config import settings
from src.models.quiz import Questions

from tests.helpers.quiz_api import QuizApiClient


@pytest.fixture
def quiz_api_client(client):
    return QuizApiClient(client, base_url=settings.API_PREFIX)


def test_read_question_success(quiz_api_client, mock_db):
    mock_question = Questions(id=1, question_text="What is the best Python Framework?")
    mock_db.query.return_value.filter.return_value.first = MagicMock(
        return_value=mock_question
    )

    response = quiz_api_client.read_question(question_id=1)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["question_text"] == "What is the best Python Framework?"


def test_read_question_not_found(quiz_api_client, mock_db):
    mock_db.query.return_value.filter.return_value.first = MagicMock(return_value=None)

    response = quiz_api_client.read_question(question_id=1)

    assert response.status_code == 404
    assert response.json()["detail"] == "Question is not found"


def test_create_question_success(quiz_api_client, mock_db):
    payload = quiz_api_client.create_question_payload(
        question_text="What is the best Python Framework?"
    )

    mock_question = Questions(id=1, question_text=payload["question_text"])

    def mock_refresh_side_effect(obj):
        obj.id = mock_question.id
        obj.question_text = mock_question.question_text
        return None

    mock_db.refresh.side_effect = mock_refresh_side_effect

    response = quiz_api_client.create_question(payload)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["question_text"] == "What is the best Python Framework?"

    # expected_calls=[
    #     call(ANY),
    #     call(ANY),
    #     call(ANY)
    # ]
    # mock_db.add.assert_has_calls(expected_calls)

    assert mock_db.add.call_count == 3
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
