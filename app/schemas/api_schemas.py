from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.orm_schemas import UserResponse


class APIHelloWorldResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: str = "Hello world!"


class APIUserResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: UserResponse


class APIUserListResponse(BaseModel):
    status: Literal['ok'] = 'ok'
    data: list[UserResponse]
