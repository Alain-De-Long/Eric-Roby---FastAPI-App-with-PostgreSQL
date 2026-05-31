from typing import List, Annotated
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.config import settings
from database.session import create_all_tables, db_dependency
from models.quiz import Quesions, Choices
from schemas.quiz import QuestionBase, ChoiceBase

create_all_tables()

app = FastAPI()


@app.post("/questions")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = Quesions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )

        db.add(db_choice)
    db.commit()


# if __name__ == "__main__":
    # print(settings.POSTGRES_DB)
    # print(settings.POSTGRES_USER)
    # print(settings.POSTGRES_PASSWORD)
    # print(settings.DATABASE_URL)
