from fastapi import FastAPI
from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router
app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "안녕하세요 파이보"}

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
