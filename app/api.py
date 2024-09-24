from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.api_schemas import (
    APIUserResponse,
    APIUserListResponse,
    APICheckUserResponse,
    APIPhoneResponse
)
from app.schemas.orm_schemas import (
    UserCreateRequest,
    UserIDCreateRequest,
    ReplacePhoneRequest,
    UserResponse,
    PhoneResponse,
    GetUserIdRequest,
    UserIdResponse
)
from app.database.orm_manager import orm_manager

from loguru import logger


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
    try:
        user = await orm_manager.get_user(user_id=user_data.user_id)
        logger.info(user)
        return JSONResponse(
            content={
                "status": "ok",
                "data": True
            }
        )
    except Exception as _ex:
        logger.info(_ex)
        return JSONResponse(
            content={
                "status": "ok",
                "data": False
            }
        )


@router.post("/get_phone/", response_model=PhoneResponse)
async def get_phone(user_data: UserIDCreateRequest) -> JSONResponse:
    phone = await orm_manager.get_phone(user_id=user_data.user_id)
    if phone is not None:
        return JSONResponse(
            content={
                "status": "ok",
                "data": phone
            }
        )


@router.post("/replace_phone/", response_model=APIUserResponse)
async def replace_phone(user_data: ReplacePhoneRequest) -> JSONResponse:
    user = await orm_manager.replace_phone(
        user_id=user_data.user_id,
        phone=user_data.phone
    )
    if user is not None:
        return JSONResponse(
            content={
                "status": "ok",
                "data": user
            }
        )


@router.post("/get_user_id/", response_model=UserResponse)
async def get_user_id(user_data: GetUserIdRequest) -> JSONResponse:
    user_id = await orm_manager.get_user_id(phone=user_data.phone)
    if user_id is not None:
        return JSONResponse(
            content={
                "status": "ok",
                "data": user_id
            }
        )


@router.get("/clear_table")
async def clear_table() -> JSONResponse:
    await orm_manager.clear_table()
    return JSONResponse(
        content={
            "status": "ok",
            "data": "table was cleared"
        }
    )
