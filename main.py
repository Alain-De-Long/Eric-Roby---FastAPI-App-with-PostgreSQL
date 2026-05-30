from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Annotated

app=FastAPI()

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool
    
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
