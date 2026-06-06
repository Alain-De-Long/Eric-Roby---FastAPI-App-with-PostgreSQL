from typing import Annotated

from core.config import settings
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception as e:
        print(f"Database error encountered: {e}")
        raise (e)
    finally:
        db.close()


def create_all_tables():
    Base.metadata.create_all(bind=engine)


db_dependency = Annotated[Session, Depends(get_db)]
