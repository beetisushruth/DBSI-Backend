from typing import Optional, List

from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
    """
    Schema for Question model
    """
    title: str = Field(...)
    accepted_answer_id: int = Field(...)
    answer_count: int = Field(...)
    comment_count: int = Field(...)
    creation_date: str = Field(...)
    favorite_count: int = Field(...)
    owner_user_id: int = Field(...)
    score: int = Field(...)
    view_count: int = Field(...)
    related_posts: List[int] = Field(...)
    tags: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "How to create a new file in Python?",
                "accepted_answer_id": 1,
                "answer_count": 1,
                "comment_count": 0,
                "creation_date": "2021-03-01T00:00:00.000Z",
                "favorite_count": 0,
                "owner_user_id": 1,
                "score": 1,
                "view_count": 1,
                "related_posts": [1, 2, 3],
                "tags": ["python", "file", "create"]
            }
        }


class UpdateQuestionModel(BaseModel):
    """
    Schema for updating a question
    """
    title: Optional[str]
    accepted_answer_id: Optional[int]
    answer_count: Optional[int]
    comment_count: Optional[int]
    creation_date: Optional[str]
    favorite_count: Optional[int]
    owner_user_id: Optional[int]
    score: Optional[int]
    view_count: Optional[int]
    related_posts: Optional[List[int]]
    tags: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "title": "How to create a new file in Python?",
                "accepted_answer_id": 1,
                "answer_count": 1,
                "comment_count": 0,
                "creation_date": "2021-03-01T00:00:00.000Z",
                "favorite_count": 0,
                "owner_user_id": 1,
                "score": 1,
                "view_count": 1,
                "related_posts": [1, 2, 3],
                "tags": ["python", "file", "create"]
            }
        }


def ResponseModel(data, message):
    """
    Schema for response model
    :param data: data to be returned
    :param message: message to be returned
    :return: response model
    """
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    """
    Schema for error response model
    :param error: error to be returned
    :param code:  code to be returned
    :param message: message to be returned
    :return: error response model
    """
    return {"error": error, "code": code, "message": message}
