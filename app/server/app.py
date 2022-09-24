from fastapi import FastAPI

from app.server.routes.question import router as QuestionRouter
from app.server.routes.answer import router as AnswerRouter
from app.server.routes.user import router as UserRouter

app = FastAPI()

app.include_router(QuestionRouter, tags=["Questions"], prefix="/question")
app.include_router(AnswerRouter, tags=["Answers"], prefix="/answer")
app.include_router(UserRouter, tags=["Users"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return """Welcome to DBSI Project API on MongoDB. Version 1.0.0. Authors: Sushruth, Koti, Dheeraj, Venkatesh. This API is used to query the StackOverflow dataset on MongoDB."""
