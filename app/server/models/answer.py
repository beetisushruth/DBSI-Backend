from typing import Optional

from pydantic import BaseModel, Field


class AnswerSchema(BaseModel):
    """
    Schema for Answer model
    """
    id: int = Field(...)
    body: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "body": "This is an example answer"
            }
        }


class UpdateAnswerModel(BaseModel):
    """
    Schema for updating an answer
    """
    id: int = Field(...)
    body: Optional[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "body": "This is an example answer"
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
    :param code: code to be returned
    :param message: message to be returned
    :return: error response model
    """
    return {"error": error, "code": code, "message": message}

