from fastapi.testclient import TestClient


class QuizApiClient:
    def __init__(self, client: TestClient, base_url: str) -> None:
        self.client = client
        self.base_url = base_url

    # QUESTIONS
    def read_all_questions(self):
        return self.client.get(f"{self.base_url}/questions/")

    def create_question(self, payload: dict):
        return self.client.post(f"{self.base_url}/questions/", json=payload)

    def read_question(self, question_id: int):
        return self.client.get(f"{self.base_url}/questions/{question_id}")

    def update_question(self, question_id: int, question_text: str):
        return self.client.put(
            f"{self.base_url}/questions/{question_id}",
            json={"question_text": question_text},
        )

    def delete_question(self, question_id: int):
        return self.client.delete(f"{self.base_url}/questions/{question_id}")

    # CHOICES
    def read_choices(self, question_id: int):
        return self.client.get(f"{self.base_url}/choices/{question_id}")

    def update_choice(self, choice_id: int, choice_text: str, is_correct: bool):
        payload = {"choice_text": choice_text, "is_correct": is_correct}
        return self.client.put(f"{self.base_url}/choices/{choice_id}", json=payload)

    def delete_choice(self, choice_id: int):
        return self.client.delete(f"{self.base_url}/choices/{choice_id}")

    # UTILITES
    @staticmethod
    def create_question_payload(**kwargs):
        base_payload = {
            "question_text": "1 + 1 = ?",
            "choices": [
                {"choice_text": "2", "is_correct": True},
                {"choice_text": "3", "is_correct": False},
            ],
        }

        base_payload.update(kwargs)
        return base_payload

    @staticmethod
    def create_choice_payload(**kwargs):
        base_payload = {"choice_text": "FastAPI is awesome", "is_correct": True}

        base_payload.update(kwargs)
        return base_payload
