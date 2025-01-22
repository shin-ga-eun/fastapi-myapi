import datetime

from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None

class AnswerCreate(BaseModel):
    content: str

    # 유효성
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다')
        return v