def test_read_question_and_its_choices_when_id_exists_returns_200(quiz_api_client):
    # Create a question
    payload = quiz_api_client.create_question_payload(
        question_text="1 + 1 = ?",
        choices=[
            {"choice_text": "2", "is_correct": True},
            {"choice_text": "3", "is_correct": False},
        ],
    )
    create_question_response = quiz_api_client.create_question(payload=payload)
    assert create_question_response.status_code == 201

    create_data = create_question_response.json()
    assert len(create_data["choices"]) == 2
    assert create_data["choices"][0]["id"] is not None
    assert create_data["choices"][1]["id"] is not None

    # Get the question, and check that it exists
    question_id = create_data["id"]
    read_question_response = quiz_api_client.read_question(question_id=question_id)
    assert read_question_response.status_code == 200

    data = read_question_response.json()
    assert data["id"] == question_id
    assert data["question_text"] == payload["question_text"]
    assert len(data["choices"]) == 2
    assert data["choices"][0]["choice_text"] == payload["choices"][0]["choice_text"]
    assert data["choices"][1]["choice_text"] == payload["choices"][1]["choice_text"]

    # Get the choices of the question, and check that they are correctly saved
    read_choices_response = quiz_api_client.read_choices(question_id=question_id)
    assert read_choices_response.status_code == 200

    choices_data = read_choices_response.json()
    assert len(choices_data) == 2

    assert choices_data[0]["choice_text"] == payload["choices"][0]["choice_text"]
    assert choices_data[0]["is_correct"] == payload["choices"][0]["is_correct"]

    assert choices_data[1]["choice_text"] == payload["choices"][1]["choice_text"]
    assert choices_data[1]["is_correct"] == payload["choices"][1]["is_correct"]


def test_read_question_and_choices_when_id_not_found_returns_404(quiz_api_client):
    read_question_response = quiz_api_client.read_question(question_id=999)
    assert read_question_response.status_code == 404
    assert read_question_response.json()["detail"] == "Question is not found"

    read_choices_repsonse = quiz_api_client.read_choices(question_id=999)
    assert read_choices_repsonse.status_code == 404
    assert read_choices_repsonse.json()["detail"] == "Choices is not found"


def test_update_and_delete_choice_standalone(quiz_api_client):
    payload = quiz_api_client.create_question_payload(
        question_text="What is the capital of Vietnam?",
        choices=[
            {"choice_text": "Hanoi", "is_correct": True},
            {"choice_text": "HCM City", "is_correct": False},
        ],
    )
    create_question_response = quiz_api_client.create_question(payload=payload)
    assert create_question_response.status_code == 201

    question_data = create_question_response.json()
    question_id = question_data["id"]

    target_choice_id = question_data["choices"][1]["id"]
    update_choice_response = quiz_api_client.update_choice(
        choice_id=target_choice_id, choice_text="Da Nang", is_correct=False
    )

    assert update_choice_response.status_code == 200
    assert update_choice_response.json()["choice_text"] == "Da Nang"

    delete_choice_response = quiz_api_client.delete_choice(choice_id=target_choice_id)
    assert delete_choice_response.status_code == 200

    read_choices_response = quiz_api_client.read_choices(question_id=question_id)
    assert read_choices_response.status_code == 200
    assert len(read_choices_response.json()) == 1


def test_cascade_delete_question_removes_choices_from_db(quiz_api_client):
    payload = quiz_api_client.create_question_payload()
    create_question_response = quiz_api_client.create_question(payload=payload)
    assert create_question_response.status_code == 201

    question_id = create_question_response.json()["id"]
    delete_question_response = quiz_api_client.delete_question(question_id=question_id)
    assert delete_question_response.status_code == 200

    read_choices_response = quiz_api_client.read_choices(question_id=question_id)
    assert read_choices_response.status_code == 404
