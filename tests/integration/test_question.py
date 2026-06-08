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
