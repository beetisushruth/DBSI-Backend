from typing import Optional, List

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    """
    Schema for User model
    """
    display_name: str = Field(...)
    creation_date: str = Field(...)
    location: str = Field(...)
    reputation: int = Field(...)
    up_votes: int = Field(...)
    down_votes: int = Field(...)
    views: int = Field(...)
    badges: int = Field(...)
    questions: List[int] = Field(...)
    answers: List[int] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "display_name": "John Doe",
                "creation_date": "2021-03-01T00:00:00.000Z",
                "location": "New York",
                "reputation": 1,
                "up_votes": 1,
                "down_votes": 1,
                "views": 1,
                "badges": 1,
                "questions": [1, 2, 3],
                "answers": [1, 2, 3]
            }
        }


class UpdateUserModel(BaseModel):
    """
    Schema for updating a user
    """
    display_name: str = Field(...)
    creation_date: str = Field(...)
    location: Optional[str] = Field(...)
    reputation: Optional[int] = Field(...)
    up_votes: Optional[int] = Field(...)
    down_votes: Optional[int] = Field(...)
    views: Optional[int] = Field(...)
    badges: Optional[int] = Field(...)
    questions: Optional[List[int]] = Field(...)
    answers: Optional[List[int]] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "display_name": "John Doe",
                "creation_date": "2021-03-01T00:00:00.000Z",
                "location": "New York",
                "reputation": 1,
                "up_votes": 1,
                "down_votes": 1,
                "views": 1,
                "badges": 1,
                "questions": [1, 2, 3],
                "answers": [1, 2, 3]
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