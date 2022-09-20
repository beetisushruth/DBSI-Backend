from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_question,
    delete_question,
    retrieve_question,
    retrieve_questions,
    update_question
)

from app.server.models.question import (
    ErrorResponseModel,
    ResponseModel,
    UpdateQuestionModel,
    QuestionSchema
)

router = APIRouter()


@router.post("/", response_description="Question data added into the database")
async def add_question_data(question: QuestionSchema = Body(...)):
    question = jsonable_encoder(question)
    new_question = await add_question(question)
    return ResponseModel(new_question, "Question added successfully.")


@router.get("/", response_description="Questions retrieved")
async def get_questions():
    questions = await retrieve_questions()
    if questions:
        return ResponseModel(questions, "Questions data retrieved successfully")
    return ResponseModel(questions, "Empty list returned")


@router.get("/{id}", response_description="Question data retrieved")
async def get_question_data(id):
    question = await retrieve_question(id)
    if question:
        return ResponseModel(question, "Question data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Question doesn't exist.")
