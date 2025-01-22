from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate, QuestionDelete
from models import Question, User
from sqlalchemy.orm import Session

from sqlalchemy import func


def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc(), Question.id.desc())

    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()

def create_dummy_question(db: Session, dummy_count: int):
    max_idx = db.query(func.max(Question.id)).scalar()
    max_idx = 1 if max_idx is None else int(max_idx)+1
    print(f'start pid is {max_idx} ...')
    for idx in range(max_idx, max_idx + dummy_count):
        db_question = Question(subject='test question subject' + str(idx),
                           content='test question content' + str(idx),
                           create_date=datetime.now())
        db.add(db_question)
        if idx%100==0:
            print(f'insert pid is {idx} ...')
    db.commit()
    print(f'... end pid is {idx} \n')
    
def update_question(db: Session, db_question:Question, question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()

def delete_question(db: Session, question_delete: QuestionDelete):
    question = db.query(Question).get(question_delete.question_id)
    db.delete(question)
    db.commit()

def delete_all_question(db: Session):
    db.query(Question).delete()
    db.commit()