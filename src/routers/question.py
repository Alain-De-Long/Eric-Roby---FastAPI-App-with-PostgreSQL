from fastapi import APIRouter, HTTPException
from src.database.session import db_dependency
from src.models.quiz import Choices, Questions
from src.schemas.quiz import QuestionBase

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/{question_id}")
def read_question(question_id: int, db: db_dependency):
    result = db.query(Questions).filter(Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")

    return result


@router.post("/", status_code=201)
def create_questions(question: QuestionBase, db: db_dependency):
    db_question = Questions(question_text=question.question_text)
    db.add(db_question)
    db.flush()

    for choice in question.choices:
        db_choice = Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )
        db.add(db_choice)

    db.commit()
    db.refresh(db_question)

    return db_question
