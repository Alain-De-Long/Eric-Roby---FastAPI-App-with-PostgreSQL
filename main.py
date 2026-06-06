from database.session import create_all_tables, db_dependency
from fastapi import FastAPI, HTTPException
from models.quiz import Choices, Questions
from schemas.quiz import QuestionBase

create_all_tables()

app = FastAPI()


@app.get("/questions/{question_id}")
def read_question(question_id: int, db: db_dependency):
    result = db.query(Questions).filter(Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")

    return result


@app.get("/choices/{question_id}")
def read_choices(question_id: int, db: db_dependency):
    result = db.query(Choices).filter(Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices is not found")

    return result


@app.post("/questions")
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


# if __name__ == "__main__":
# print(settings.POSTGRES_DB)
# print(settings.POSTGRES_USER)
# print(settings.POSTGRES_PASSWORD)
# print(settings.DATABASE_URL)
