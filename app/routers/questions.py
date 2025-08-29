from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, dependencies

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/", response_model=list[schemas.Question])
def read_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.question_crud.get_questions(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Question, status_code=status.HTTP_201_CREATED)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(database.get_db)
):
    return crud.question_crud.create_question(db, question)

@router.get("/{question_id}", response_model=schemas.QuestionWithAnswers)
def read_question(
    question: schemas.Question = Depends(dependencies.get_question_or_404)
):
    return question

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int,
    db: Session = Depends(database.get_db)
):
    if not crud.question_crud.delete_question(db, question_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )