from fastapi import FastAPI

from src.core.config import settings
from src.database.session import create_all_tables
from src.routers import choice, question

create_all_tables()

app = FastAPI(
    title="FastAPI PostgreSQL",
    description="Build a FastAPI app with PostgreSQL",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(question.router, prefix=settings.API_PREFIX)
app.include_router(choice.router, prefix=settings.API_PREFIX)
