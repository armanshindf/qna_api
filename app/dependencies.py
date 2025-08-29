from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import crud, database

def get_question_or_404(question_id: int, db: Session = Depends(database.get_db)):
    question = crud.question_crud.get_question(db, question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return question

def get_answer_or_404(answer_id: int, db: Session = Depends(database.get_db)):
    answer = crud.answer_crud.get_answer(db, answer_id)
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    return answer