from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, dependencies

router = APIRouter(prefix="/questions/{question_id}/answers", tags=["answers"])

@router.post("/", response_model=schemas.Answer, status_code=status.HTTP_201_CREATED)
def create_answer(
    question_id: int,
    answer: schemas.AnswerCreate,
    db: Session = Depends(database.get_db),
    question: schemas.Question = Depends(dependencies.get_question_or_404)
):
    return crud.answer_crud.create_answer(db, answer, question_id)

@router.get("/{answer_id}", response_model=schemas.Answer)
def read_answer(
    answer: schemas.Answer = Depends(dependencies.get_answer_or_404)
):
    return answer

@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    answer_id: int,
    db: Session = Depends(database.get_db)
):
    if not crud.answer_crud.delete_answer(db, answer_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )