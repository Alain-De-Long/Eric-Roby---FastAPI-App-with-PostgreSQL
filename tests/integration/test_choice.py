def test_read_choices_by_question_id(quiz_api_client):
    payload = quiz_api_client.create_question_payload(
        question_text="What is the Python Framework?",
        choices=[
            {"choice_text": "FastAPI", "is_correct": True},
            {"choice_text": "React", "is_correct": False},
        ],
    )

    create_question_response = quiz_api_client.create_question(payload=payload)
    assert create_question_response.status_code == 201

    question_id = create_question_response.json()["id"]
    read_choices_response = quiz_api_client.read_choices(question_id=question_id)
    assert read_choices_response.status_code == 200

    choices_data = read_choices_response.json()
    assert len(choices_data) == 2
    assert choices_data[0]["choice_text"] == "FastAPI"
    assert choices_data[0]["is_correct"] is True
    assert choices_data[1]["choice_text"] == "React"
    assert choices_data[1]["is_correct"] is False


def test_update_choice_standalone(quiz_api_client):
    payload = quiz_api_client.create_question_payload(
        question_text="2 + 2 = ?",
        choices=[
            {"choice_text": "4", "is_correct": True},
            {"choice_text": "5", "is_correct": False},
        ],
    )
    create_question_response = quiz_api_client.create_question(payload=payload)
    assert create_question_response.status_code == 201

    question_data = create_question_response.json()
    target_choice_id = question_data["choices"][1]["id"]

    update_choice_response = quiz_api_client.update_choice(
        choice_id=target_choice_id, choice_text="All of above", is_correct=False
    )
    assert update_choice_response.status_code == 200

    updated_data = update_choice_response.json()
    assert updated_data["id"] == target_choice_id
    assert updated_data["choice_text"] == "All of above"
    assert updated_data["is_correct"] is False


def test_delete_choice_standalone(quiz_api_client):
    payload = quiz_api_client.create_question_payload()
    create_question_response = quiz_api_client.create_question(payload=payload)
    assert create_question_response.status_code == 201

    create_question_data = create_question_response.json()
    question_id = create_question_data["id"]
    target_choice_id = create_question_data["choices"][0]["id"]

    delete_choice_response = quiz_api_client.delete_choice(choice_id=target_choice_id)
    assert delete_choice_response.status_code == 200
    assert (
        delete_choice_response.json()["detail"]
        == f"Choice {target_choice_id} has been succesfully deleted"
    )

    read_question_response = quiz_api_client.read_choices(question_id=question_id)
    assert read_question_response.status_code == 200
    assert len(read_question_response.json()) == 1
