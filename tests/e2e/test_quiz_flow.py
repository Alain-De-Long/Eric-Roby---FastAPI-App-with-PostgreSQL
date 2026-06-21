def test_quiz_management_flow(quiz_api_client):
    # 1. CREATE
    payload = quiz_api_client.create_question_payload(
        question_text="What is the default port of FastAPI?",
        choices=[
            {"choice_text": "3000", "is_correct": False},
            {"choice_text": "8000", "is_correct": True},
        ],
    )
    create_question_response = quiz_api_client.create_question(payload=payload)
    assert create_question_response.status_code == 201

    question_data = create_question_response.json()
    question_id = question_data["id"]
    target_choice_id = question_data["choices"][0]["id"]

    # 2. READ
    read_question_response = quiz_api_client.read_question(question_id=question_id)
    assert read_question_response.status_code == 200
    assert read_question_response.json()["question_text"] == payload["question_text"]

    # 3. UPDATE QUESTION
    updated_text = "What is the default port of Uvicorn/FastAPI?"
    update_question_response = quiz_api_client.update_question(
        question_id=question_id, question_text=updated_text
    )
    assert update_question_response.status_code == 200
    assert update_question_response.json()["question_text"] == updated_text

    # 4. UPDATE CHOICE
    update_choice_response = quiz_api_client.update_choice(
        choice_id=target_choice_id, choice_text="5173", is_correct=False
    )
    assert update_choice_response.status_code == 200
    assert update_choice_response.json()["choice_text"] == "5173"

    # 5. DELETE & VERIFY CASCADE
    delete_question_response = quiz_api_client.delete_question(question_id=question_id)
    assert delete_question_response.status_code == 200

    final_check_response = quiz_api_client.read_question(question_id=question_id)
    assert final_check_response.status_code == 404
