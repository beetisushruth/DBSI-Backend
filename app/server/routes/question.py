from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_question,
    delete_question,
    retrieve_question,
    retrieve_questions,
    update_question,
    retrieve_questions_by_aggregation_pipeline
)

from app.server.models.question import (
    ErrorResponseModel,
    ResponseModel,
    UpdateQuestionModel,
    QuestionSchema
)

router = APIRouter()


# Basic CRUD operations

@router.post("/add", response_description="Question data added into the database")
async def add_question_data(question: QuestionSchema = Body(...)):
    question = jsonable_encoder(question)
    new_question = await add_question(question)
    return ResponseModel(new_question, "Question added successfully.")


@router.get("/all/{count}", response_description="Questions retrieved")
async def get_questions(count: int):
    questions = await retrieve_questions(count)
    if questions:
        return ResponseModel(questions, "Questions data retrieved successfully")
    return ResponseModel(questions, "Empty list returned")


@router.get("/{id}", response_description="Question data retrieved")
async def get_question_data(id):
    question = await retrieve_question(id)
    if question:
        return ResponseModel(question, "Question data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Question doesn't exist.")


@router.post("/update", response_description="Question data updated in the database")
async def update_question_data(req: UpdateQuestionModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    if 'id' not in req:
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the question data.",
        )
    # print(req)
    updated_question = await update_question(req['id'], req)
    if updated_question:
        return ResponseModel(
            "Question with ID: {} update is successful".format(req['id']),
            "Question name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the question data.",
    )


@router.delete("/{id}", response_description="Question data deleted from the database")
async def delete_question_data(id: str):
    deleted_question = await delete_question(id)
    if deleted_question:
        return ResponseModel(
            "Question with ID: {} removed".format(id), "Question deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Question with id {0} doesn't exist".format(id)
    )


# Advanced queries
# aggregate pipelines
popular_unanswered_questions_by_tag = [
    {
        '$match': {
            'tags': {
                '$exists': True
            },
            'accepted_answer_id': {
                '$exists': False
            }
        }
    }, {
        '$unwind': {
            'path': '$tags'
        }
    }, {
        '$match': {
            'tags': {
                '$eq': 'python'
            }
        }
    }, {
        '$sort': {
            'view_count': -1
        }
    }, {
        '$limit': 10
    }
]


@router.get("/popular-unanswered-questions-by-tag/{tag}/{count}", response_description="Questions retrieved")
async def get_popular_unanswered_questions_by_tag(tag: str, count: str):
    popular_unanswered_questions_by_tag[2]['$match']['tags']['$eq'] = tag
    popular_unanswered_questions_by_tag[4]['$limit'] = int(count)
    questions = await retrieve_questions_by_aggregation_pipeline(popular_unanswered_questions_by_tag)
    if questions:
        return ResponseModel(questions, "Questions data retrieved successfully")
    return ResponseModel(questions, "Empty list returned")


answered_questions_for_tag = [
    {
        '$match': {
            'tags': {
                '$exists': True
            }
        }
    }, {
        '$unwind': {
            'path': '$tags'
        }
    }, {
        '$match': {
            'tags': 'python',
            'accepted_answer_id': {
                '$exists': True
            }
        }
    }, {
        '$group': {
            '_id': None,
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 0
        }
    }
]


@router.get("/answered-questions-for-tag/{tag}", response_description="Questions retrieved")
async def get_answered_questions_for_tag(tag: str):
    answered_questions_for_tag[2]['$match']['tags'] = tag
    questions = await retrieve_questions_by_aggregation_pipeline(answered_questions_for_tag)
    if questions:
        return ResponseModel(questions, "Questions data retrieved successfully")
    return ResponseModel(questions, "Empty list returned")
