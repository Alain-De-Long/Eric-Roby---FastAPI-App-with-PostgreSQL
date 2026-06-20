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


def test_update_choice_success(quiz_api_client, mock_db):
    mock_choice = Choices(id=1, choice_text="Old Text", is_correct=False, question_id=1)
    mock_db.query.return_value.filter().first.return_value = mock_choice

    new_text = "Updated Text"

    def mock_refresh_side_effect(obj):
        obj.id = 1
        obj.choice_text = new_text
        obj.is_correct = True
        return None

    mock_db.refresh.side_effect = mock_refresh_side_effect

    response = quiz_api_client.update_choice(
        choice_id=1, choice_text=new_text, is_correct=True
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["choice_text"] == new_text
    assert data["is_correct"] is True

    mock_db.query.assert_called_once_with(Choices)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_update_choice_not_found(quiz_api_client, mock_db):
    mock_db.query.return_value.filter().first.return_value = None

    response = quiz_api_client.update_choice(
        choice_id=999, choice_text="Random", is_correct=False
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Choice is not found"

    mock_db.query.assert_called_once_with(Choices)
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()


def test_delete_choice_success(quiz_api_client, mock_db):
    mock_choice = Choices(
        id=1, choice_text="Irrelevant Choice", is_correct=True, question_id=1
    )
    mock_db.query.return_value.filter().first.return_value = mock_choice

    response = quiz_api_client.delete_choice(choice_id=1)

    assert response.status_code == 200
    assert response.json()["detail"] == "Choice 1 has been succesfully deleted"

    mock_db.query.assert_called_once_with(Choices)
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()


def test_delete_choice_not_found(quiz_api_client, mock_db):
    mock_db.query.return_value.filter().first.return_value = None

    response = quiz_api_client.delete_choice(choice_id=999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Choice is not found"

    mock_db.query.assert_called_once_with(Choices)
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()
