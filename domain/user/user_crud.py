from datetime import datetime

from passlib.context import CryptContext
from models import User
from sqlalchemy.orm import Session

from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# user 객체를 생성한다.
def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                    password=pwd_context.hash(user_create.password1),
                    email=user_create.email)
    db.add(db_user)
    db.commit()

# user 기존 객체와 비교 후 존재시 반환한다.
def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

# user 기존 객체와 비교 후 존재시 반환한다.
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()