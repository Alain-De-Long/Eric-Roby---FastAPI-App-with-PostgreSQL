from fastapi import APIRouter, HTTPException
from src.database.session import db_dependency
from src.models.quiz import Choices, Questions
from src.schemas.quiz import QuestionRequest, QuestionResponse

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/{question_id}")
def read_question(question_id: int, db: db_dependency):
    result = db.query(Questions).filter(Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")

    return result


@router.post("/", status_code=201, response_model=QuestionResponse)
def create_questions(question: QuestionRequest, db: db_dependency):
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


@router.put("/{question_id}", status_code=200)
def update_question(question_id: int, updated_data: QuestionRequest, db: db_dependency):
    db_quesion = db.query(Questions).filter(Questions.id == question_id).first()
    if not db_quesion:
        raise HTTPException(status_code=404, detail="Question is not found")

    db_quesion.question_text = updated_data.question_text

    db.commit()
    db.refresh(db_quesion)
    return db_quesion


@router.delete("/{question_id}", status_code=200)
def delete_question(question_id: int, db: db_dependency):
    db_question = db.query(Questions).filter(Questions.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question is not found")

    db.query(Choices).filter(Choices.question_id == question_id).delete(
        synchronize_session=False
    )

    db.delete(db_question)

    db.commit()

    return {
        "detail": (
            f"Question {question_id} and its choices have been successfully deleted"
        )
    }
