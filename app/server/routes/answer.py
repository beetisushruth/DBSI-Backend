from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_answer,
    delete_answer,
    retrieve_answer,
    retrieve_answers,
    update_answer,
    retrieve_answers_by_aggregation_pipeline
)

from app.server.models.answer import (
    ErrorResponseModel,
    ResponseModel,
    UpdateAnswerModel,
    AnswerSchema
)

router = APIRouter()


# Basic CRUD operations

@router.post("/", response_description="Answer data added into the database")
async def add_answer_data(answer: AnswerSchema = Body(...)):
    answer = jsonable_encoder(answer)
    new_answer = await add_answer(answer)
    return ResponseModel(new_answer, "Answer added successfully.")


@router.get("/all/{count}", response_description="Answers retrieved")
async def get_answers(count: int):
    answers = await retrieve_answers(count)
    if answers:
        return ResponseModel(answers, "Answers data retrieved successfully")
    return ResponseModel(answers, "Empty list returned")


@router.get("/{id}", response_description="Answer data retrieved")
async def get_answer_data(id):
    answer = await retrieve_answer(id)
    if answer:
        return ResponseModel(answer, "Answer data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Answer doesn't exist.")


@router.post("/", response_description="Answer data updated in the database")
async def update_answer_data(id: str, req: UpdateAnswerModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_answer = await update_answer(id, req)
    if updated_answer:
        return ResponseModel(
            "Answer with ID: {} name update is successful".format(id),
            "Answer name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the answer data.",
    )


@router.delete("/{id}", response_description="Answer data deleted from the database")
async def delete_answer_data(id: str):
    deleted_answer = await delete_answer(id)
    if deleted_answer:
        return ResponseModel(
            "Answer with ID: {} removed".format(id), "Answer deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Answer with id {0} doesn't exist".format(id)
    )
