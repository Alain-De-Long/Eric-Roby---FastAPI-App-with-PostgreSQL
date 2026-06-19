from pydantic import BaseModel, ConfigDict


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class ChoiceResponse(ChoiceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class QuestionBase(BaseModel):
    question_text: str


class QuestionRequest(QuestionBase):
    choices: list[ChoiceBase]


class QuestionResponse(QuestionBase):
    id: int
    choices: list[ChoiceResponse]

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    detail: str
