from pydantic import BaseModel, ConfigDict, Field


class UserCreateRequest(BaseModel):
    user_id: int
    username: str
    telefon: str = Field(max_length=15)


class UserIDCreateRequest(BaseModel):
    user_id: int


class ReplacePhoneRequest(BaseModel):
    user_id: int
    phone: str


class UserResponse(BaseModel):
    id: int
    user_id: int
    username: str
    telefon: str

    model_config = ConfigDict(from_attributes=True)


class PhoneResponse(BaseModel):
    phone: str

    model_config = ConfigDict(from_attributes=True)
