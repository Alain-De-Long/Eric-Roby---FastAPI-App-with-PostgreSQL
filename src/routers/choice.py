from fastapi import APIRouter, HTTPException
from src.database.session import db_dependency
from src.models.quiz import Choices
from src.schemas.quiz import ChoiceBase, ChoiceResponse, DeleteResponse

router = APIRouter(prefix="/choices", tags=["choices"])


@router.get("/{question_id}", status_code=200, response_model=list[ChoiceResponse])
def read_choices(question_id: int, db: db_dependency):
    result = db.query(Choices).filter(Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices is not found")

    return result


@router.put("/{choice_id}", status_code=200, response_model=ChoiceResponse)
def update_choice(choice_id: int, updated_data: ChoiceBase, db: db_dependency):
    db_choice = db.query(Choices).filter(Choices.id == choice_id).first()
    if not db_choice:
        raise HTTPException(status_code=404, detail="Choice is not found")

    db_choice.choice_text = updated_data.choice_text
    db_choice.is_correct = updated_data.is_correct

    db.commit()
    db.refresh(db_choice)

    return db_choice


@router.delete("/{choice_id}", status_code=200, response_model=DeleteResponse)
def delete_choice(choice_id: int, db: db_dependency):
    db_choice = db.query(Choices).filter(Choices.id == choice_id).first()
    if not db_choice:
        raise HTTPException(status_code=404, detail="Choice is not found")

    db.delete(db_choice)
    db.commit()

    return {"detail": f"Choice {choice_id} has been succesfully deleted"}
