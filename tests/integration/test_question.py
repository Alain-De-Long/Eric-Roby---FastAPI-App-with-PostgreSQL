def test_create_question_success_returns_200(integration_quiz_api):
    payload = integration_quiz_api.create_question_payload()

    response = integration_quiz_api.create_question(payload=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["question_text"] == payload["question_text"]


def test_read_question_when_id_exists_returns_200(integration_quiz_api):
    # Create a question
    payload = integration_quiz_api.create_question_payload()
    create_question_response = integration_quiz_api.create_question(payload=payload)
    assert create_question_response.status_code == 201

    # Get the question, and check that it exists
    question_id = create_question_response.json()["id"]
    read_question_response = integration_quiz_api.read_question(question_id=question_id)

    assert read_question_response.status_code == 200
    assert read_question_response.json()["question_text"] == payload["question_text"]


def test_read_question_and_its_choices_when_id_exists_returns_200(integration_quiz_api):
    # Create a question
    payload = integration_quiz_api.create_question_payload(
        payload={
            "question_text": "1 + 1 = ?",
            "choices": [
                {"choice_text": "2", "is_correct": True},
                {"choice_text": "3", "is_correct": False},
            ],
        }
    )
    create_question_response = integration_quiz_api.create_question(payload=payload)
    assert create_question_response.status_code == 201

    # Get the question, and check that it exists
    question_id = create_question_response.json()["id"]
    read_question_response = integration_quiz_api.read_question(question_id=question_id)
    assert read_question_response.status_code == 200

    data = read_question_response.json()
    assert data["id"] == question_id
    assert data["question_text"] == payload["question_text"]

    # Get the choices of the question, and check that they are correctly saved
    read_choices_response = integration_quiz_api.read_choices(question_id=question_id)
    assert read_choices_response.status_code == 200

    choices_data = read_choices_response.json()
    assert len(choices_data) == 2

    assert choices_data[0]["choice_text"] == payload["choices"][0]["choice_text"]
    assert choices_data[0]["is_correct"] == payload["choices"][0]["is_correct"]

    assert choices_data[1]["choice_text"] == payload["choices"][1]["choice_text"]
    assert choices_data[1]["is_correct"] == payload["choices"][1]["is_correct"]
