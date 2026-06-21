from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.core.config import settings

_engine = None
_SessionLocal = None


class Base(DeclarativeBase):
    pass


def get_engine():
    """Get the SQLAlchemy database engine using lazy initialization"""
    global _engine
    if _engine is None:
        _engine = create_engine(settings.DATABASE_URL)

    return _engine


def get_session_local():
    """Get the SQLAlchemy session factory using lazy initialization"""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )

    return _SessionLocal


def get_db():
    Session = get_session_local()
    db = Session()

    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    Base.metadata.create_all(bind=get_engine())


db_dependency = Annotated[Session, Depends(get_db)]
