from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from typing import List, Optional

class QuestionCRUD:
    def get_questions(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Question]:
        return db.scalars(select(models.Question).offset(skip).limit(limit)).all()

    def get_question(self, db: Session, question_id: int) -> Optional[models.Question]:
        return db.get(models.Question, question_id)

    def create_question(self, db: Session, question: schemas.QuestionCreate) -> models.Question:
        db_question = models.Question(text=question.text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    def delete_question(self, db: Session, question_id: int) -> bool:
        question = self.get_question(db, question_id)
        if question:
            db.delete(question)
            db.commit()
            return True
        return False

class AnswerCRUD:
    def get_answers_by_question(self, db: Session, question_id: int) -> List[models.Answer]:
        return db.scalars(select(models.Answer).where(models.Answer.question_id == question_id)).all()

    def get_answer(self, db: Session, answer_id: int) -> Optional[models.Answer]:
        return db.get(models.Answer, answer_id)

    def create_answer(self, db: Session, answer: schemas.AnswerCreate, question_id: int) -> models.Answer:
        db_answer = models.Answer(
            text=answer.text,
            user_id=answer.user_id,
            question_id=question_id
        )
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
        return db_answer

    def delete_answer(self, db: Session, answer_id: int) -> bool:
        answer = self.get_answer(db, answer_id)
        if answer:
            db.delete(answer)
            db.commit()
            return True
        return False

question_crud = QuestionCRUD()
answer_crud = AnswerCRUD()