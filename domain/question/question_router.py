from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
# from database import SessionLocal
from domain.question import question_schema, question_crud
from models import Question, User
from domain.user.user_router import get_current_user

router = APIRouter(
    prefix="/api/question",
)

# 방법 1 ) SessionLocal 사용
# @router.get("/list")
# def question_list():
#     db = SessionLocal()
#     _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     db.close() #세션 커넥션 풀 반환
#     return _question_list

# 방법 2 ) 제너레이터, with 사용
# @router.get("/list")
# def question_list():
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     return _question_list

# 방법 3 ) 제너레이터, Depends 사용
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int=0, size: int=10): #db 객체가 Session 타입임
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'question_list': _question_list
    }

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int,
                    db: Session = Depends(get_db)):
    _question = question_crud.get_question(db, question_id= question_id)
    return _question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create, user=current_user)

@router.post("/create/dummy/{dummy_count}", status_code=status.HTTP_204_NO_CONTENT)
def dummy_question_create(dummy_count: int,
                        db: Session = Depends(get_db)):
    question_crud.create_dummy_question(db=db, dummy_count=dummy_count)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question not found"
        )

    try:
        if db_question.user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question owner not found"
            )
        if current_user.id != db_question.user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not the owner of this question"
            )
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type mismatch when comparing userIDs"
        )

    question_crud.update_question(db=db, db_question=db_question, question_update= _question_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)

    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question not found"
        )
    try:
        if db_question.user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question owner not found"
            )
        if current_user.id != db_question.user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not the owner of this question"
            )
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type mismatch when comparing userIDs"
        )
    question_crud.delete_question(db=db, question_delete=_question_delete)

@router.delete("/deleteAll")
def question_delete_all(db: Session = Depends(get_db)):
    question_crud.delete_all_question(db=db)