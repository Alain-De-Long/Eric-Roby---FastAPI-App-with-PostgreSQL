from fastapi import APIRouter, HTTPException
from src.database.session import db_dependency
from src.models.quiz import Choices

router = APIRouter(prefix="/choices", tags=["choices"])


@router.get("/{question_id}")
def read_choices(question_id: int, db: db_dependency):
    result = db.query(Choices).filter(Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices is not found")

    return result
