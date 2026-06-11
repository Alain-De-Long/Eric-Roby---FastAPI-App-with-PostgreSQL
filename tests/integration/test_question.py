def test_read_question_and_its_choices_when_id_exists_returns_200(integration_quiz_api):
    # Create a question
    payload = integration_quiz_api.create_question_payload(
        question_text="1 + 1 = ?",
        choices=[
            {"choice_text": "2", "is_correct": True},
            {"choice_text": "3", "is_correct": False},
        ],
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


def test_read_question_and_choices_when_id_not_found_returns_404(integration_quiz_api):
    read_question_response = integration_quiz_api.read_question(question_id=999)
    assert read_question_response.status_code == 404
    assert read_question_response.json()["detail"] == "Question is not found"

    read_choices_repsonse = integration_quiz_api.read_choices(question_id=999)
    assert read_choices_repsonse.status_code == 404
    assert read_choices_repsonse.json()["detail"] == "Choices is not found"
