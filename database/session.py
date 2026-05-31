from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        print("SUCCESS")
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()


def create_all_tables():
    Base.metadata.create_all(bind=engine)


db_dependency = Annotated[Session, Depends(get_db)]
