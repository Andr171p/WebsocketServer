from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.api_schemas import (
    APIUserResponse,
    APIUserListResponse,
    APICheckUserResponse
)
from app.schemas.orm_schemas import (
    UserCreateRequest,
    UserIDCreateRequest,
    UserResponse
)
from app.database.orm_manager import orm_manager


router = APIRouter()


@router.get("/")
async def get_hello_world() -> JSONResponse:
    return JSONResponse(
        content={
            "status": "ok",
            "data": "Hello world!"
        },
    )


@router.post("/get_user/", response_model=APIUserResponse)
async def get_user(user_data: UserIDCreateRequest) -> JSONResponse:
    user = await orm_manager.get_user(user_id=user_data.user_id)
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


@router.get("/get_users/", response_model=APIUserListResponse)
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


@router.post("/create_user/", response_model=APIUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateRequest) -> JSONResponse:
    user_candidate = await orm_manager.create_user(
        user_id=user_data.user_id,
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


@router.post("/check_user/", response_model=APICheckUserResponse)
async def check_user(user_data: UserIDCreateRequest) -> JSONResponse:
    user = await orm_manager.get_user(user_id=user_data.user_id)
    if not user:
        return JSONResponse(
            content={
                "status": "ok",
                "data": False
            }
        )
    else:
        return JSONResponse(
            content={
                "status": "ok",
                "data": True
            }
        )
