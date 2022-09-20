from fastapi import FastAPI

from app.server.routes.question import router as QuestionRouter

app = FastAPI()

app.include_router(QuestionRouter, tags=["Questions"], prefix="/question")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get("/getQuestion/{item_id}", tags=["Items"])
async def read_item(item_id: int):
    return {"item_id": item_id}
