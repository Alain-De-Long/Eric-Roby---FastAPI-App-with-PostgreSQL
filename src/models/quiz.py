from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base


class Questions(Base):
    __tablename__ = "questions"

    # id = Column(Integer, primary_key=True, index=True)
    # question_text = Column(String, index=True)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    question_text: Mapped[str] = mapped_column(String, index=True)

    choices: Mapped[list["Choices"]] = relationship(
        back_populates="question", cascade="all, delete-orphan", lazy="selectin"
    )


class Choices(Base):
    __tablename__ = "choices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    choice_text: Mapped[str] = mapped_column(String, index=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    question: Mapped[Questions] = relationship(back_populates="choices")
