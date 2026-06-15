from src.models.quiz import Questions


def test_read_question_success(quiz_api_client, mock_db):
    mock_question = Questions(id=1, question_text="What is the best Python Framework?")
    # mock_db.query.return_value.filter.return_value.first = MagicMock(
    #     return_value=mock_question
    # )
    mock_db.query.return_value.filter().first.return_value = mock_question

    response = quiz_api_client.read_question(question_id=1)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["question_text"] == "What is the best Python Framework?"

    mock_db.query.assert_called_once_with(Questions)


def test_read_question_not_found(quiz_api_client, mock_db):
    mock_db.query.return_value.filter().first.return_value = None

    response = quiz_api_client.read_question(question_id=999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Question is not found"

    mock_db.query.assert_called_once_with(Questions)


def test_create_question_success(quiz_api_client, mock_db):
    payload = quiz_api_client.create_question_payload(
        question_text="What is the best Python Framework?",
        choices=[
            {"choice_text": "FastAPI", "is_correct": True},
            {"choice_text": "Anything else", "is_correct": False},
        ],
    )

    mock_question = Questions(id=1, question_text=payload["question_text"])

    def mock_refresh_side_effect(obj):
        obj.id = mock_question.id
        obj.question_text = mock_question.question_text
        return None

    mock_db.refresh.side_effect = mock_refresh_side_effect

    response = quiz_api_client.create_question(payload)
    assert response.status_code == 201

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


def test_update_question_success(quiz_api_client, mock_db):
    mock_question = Questions(id=1, question_text="1 + 1 = ?")
    mock_db.query.return_value.filter().first.return_value = mock_question

    new_question_text = "2 + 2 = ?"
    response = quiz_api_client.update_question(
        question_id=1, question_text=new_question_text
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["question_text"] == new_question_text

    mock_db.query.assert_called_once_with(Questions)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_update_question_not_found(quiz_api_client, mock_db):
    mock_db.query.return_value.filter().first.return_value = None

    response = quiz_api_client.update_question(
        question_id=999, question_text="2 + 2 = ?"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Question is not found"

    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()
