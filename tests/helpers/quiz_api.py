from fastapi.testclient import TestClient


class QuizApiClient:
    def __init__(self, client: TestClient, base_url: str) -> None:
        self.client = client
        self.base_url = base_url

    def create_question(self, payload: dict):
        return self.client.post(f"{self.base_url}/questions/", json=payload)

    def read_question(self, question_id: int):
        return self.client.get(f"{self.base_url}/questions/{question_id}")

    def read_choices(self, question_id):
        return self.client.get(f"{self.base_url}/choices/{question_id}")

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
