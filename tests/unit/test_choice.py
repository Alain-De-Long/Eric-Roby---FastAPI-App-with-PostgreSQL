from unittest.mock import MagicMock

from src.models.quiz import Choices


def test_read_choices_success(quiz_api_client, mock_db):
    mock_choices = [
        Choices(id=1, question_id=1, choice_text="FastAPI", is_correct=True),
        Choices(id=2, question_id=1, choice_text="Django", is_correct=False),
    ]

    mock_db.query.return_value.filter.return_value.all = MagicMock(
        return_value=mock_choices
    )

    response = quiz_api_client.read_choices(question_id=1)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["choice_text"] == "FastAPI"
    assert data[1]["choice_text"] == "Django"
    assert data[0]["is_correct"] is True
    assert data[1]["is_correct"] is False

    mock_db.query.assert_called_once_with(Choices)


def test_read_choices_not_found(quiz_api_client, mock_db):
    mock_db.query.return_value.filter.return_value.all = MagicMock(return_value=[])

    response = quiz_api_client.read_choices(question_id=999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Choices is not found"

    mock_db.query.assert_called_once_with(Choices)
