from typing import List

from pydantic import BaseModel, ConfigDict


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionRequest(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


class ChoiceResponse(BaseModel):
    id: int
    choice_text: str
    is_correct: bool
    question_id: int

    model_config = ConfigDict(from_attributes=True)


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    choices: list[ChoiceResponse]

    model_config = ConfigDict(from_attributes=True)
