from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.api_schemas import (
    APIUserResponse,
    APIUserListResponse
)
from app.schemas.orm_schemas import (
    UserCreateRequest,
    UserResponse
)
from app.database.orm_manager import orm_manager


router = APIRouter()


@router.get("/{user_id}/", response_model=APIUserResponse)
async def get_user(user_id: int) -> JSONResponse:
    user = await orm_manager.get_user(user_id=user_id)
    if not user:
        return JSONResponse(
            content={"status": "error", "message": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    response_model = UserResponse.model_validate(user)
    return JSONResponse(
        content={
            "status": "ok",
            "data": response_model.model_dump(),
        }
    )


@router.get("/users/", response_model=APIUserListResponse)
async def get_users() -> JSONResponse:
    users = await orm_manager.get_users()
    response_data = [
        UserResponse.model_validate(u).model_dump() for u in users
    ]
    return JSONResponse(
        content={
            "status": "ok",
            "data": response_data,
        }
    )


@router.post("/user/", response_model=APIUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateRequest) -> JSONResponse:
    user_candidate = orm_manager.create_user(
        user_id=int(user_data.user_id),
        username=user_data.username,
        telefon=user_data.telefon
    )
    response_model = UserResponse.model_validate(user_candidate)
    return JSONResponse(
        content={
            "status": "ok",
            "data": response_model.model_dump(),
        },
        status_code=status.HTTP_201_CREATED,
    )
